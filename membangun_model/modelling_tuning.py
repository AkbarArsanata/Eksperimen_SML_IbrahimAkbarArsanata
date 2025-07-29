import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import mlflow
import mlflow.sklearn # Tetap diimpor untuk potensi penggunaan lain atau jika fitur diperbarui
import numpy as np
import os
import joblib # Untuk menyimpan model secara lokal
import dagshub

# --- ATUR TRACKING URI DI SINI ---
# Pastikan Anda sudah login ke DagsHub dan repo 'machine-learning-design' sudah ada di akun Anda.
# Ganti 'akbararsanata' dengan username DagsHub Anda
# Ganti 'machine-learning-design' dengan nama repository DagsHub Anda
dagshub.init(repo_owner='akbararsanata',
             repo_name='machine-learning-design',
             mlflow=True)

# MLflow Tracking URI akan diatur secara otomatis oleh dagshub.init
# ---------------------------------

# --- 1. Memuat Data ---
# Pastikan 'churn_train_preprocessed.csv' dan 'churn_test_preprocessed.csv' ada di direktori yang sama
try:
    df_train = pd.read_csv('churn_train_preprocessed.csv') # Data pelatihan Anda
    df_val = pd.read_csv('churn_test_preprocessed.csv')   # Data validasi Anda
except FileNotFoundError:
    print("Pastikan file 'churn_train_preprocessed.csv' dan 'churn_test_preprocessed.csv' ada di direktori yang sama.")
    exit() # Keluar jika file tidak ditemukan

print("Data train head:\n", df_train.head())
print("Data validation head:\n", df_val.head())

# --- 2. Split Data (X dan y) ---
# 'Exited' adalah kolom target (y)
X_train = df_train.drop('Exited', axis=1)
y_train = df_train['Exited']

X_val = df_val.drop('Exited', axis=1)
y_val = df_val['Exited']

# Pastikan kolom X_train dan X_val sama
if not X_train.columns.equals(X_val.columns):
    common_cols = list(set(X_train.columns) & set(X_val.columns))
    X_train = X_train[common_cols]
    X_val = X_val[common_cols]
    print("Kolom disesuaikan agar cocok antara X_train dan X_val.")

# Menonaktifkan MLflow autologging untuk scikit-learn
# Ini memastikan kita memiliki kontrol penuh atas logging metrik dan parameter
mlflow.sklearn.autolog(disable=True)

# --- 3. Hyperparameter Tuning untuk Random Forest dengan MLflow Tracking UI ---

model_name = "Random Forest Classifier"

# Definisikan grid parameter untuk Random Forest
# Anda bisa menyesuaikan nilai-nilai ini untuk eksplorasi yang lebih luas atau lebih detail
param_grid = {
    'n_estimators': [100, 200, 300],  # Jumlah pohon dalam forest
    'max_depth': [None, 10, 20],      # Kedalaman maksimum pohon
    'min_samples_leaf': [1, 2, 4],    # Jumlah minimum sampel yang dibutuhkan untuk menjadi daun node
    'criterion': ['gini', 'entropy']  # Fungsi untuk mengukur kualitas split
}

# Inisialisasi model Random Forest dasar
base_model = RandomForestClassifier(random_state=42)

# Gunakan GridSearchCV untuk mencari hyperparameter terbaik
# n_jobs=-1 akan menggunakan semua core CPU yang tersedia
# scoring bisa disesuaikan, misalnya 'roc_auc' jika Anda lebih memprioritaskan area di bawah kurva ROC
grid_search = GridSearchCV(estimator=base_model,
                           param_grid=param_grid,
                           cv=3, # Jumlah lipatan cross-validation
                           scoring='f1_weighted', # Metrik untuk memilih model terbaik selama CV
                           n_jobs=-1,
                           verbose=2) # Verbose level untuk melihat progres

print(f"\n--- Memulai Hyperparameter Tuning untuk {model_name} ---")

# Mulai MLflow run untuk proses tuning
with mlflow.start_run(run_name=f"{model_name}_Hyperparameter_Tuning_DagsHub"):
    # Log ukuran dataset sebagai parameter
    mlflow.log_param("training_set_size", len(X_train))
    mlflow.log_param("validation_set_size", len(X_val))
    mlflow.log_param("tuning_method", "GridSearchCV")
    mlflow.log_param("cv_folds", grid_search.cv)
    mlflow.log_param("scoring_metric_for_cv", grid_search.scoring)

    # Log grid parameter yang digunakan
    for param, values in param_grid.items():
        mlflow.log_param(f"param_grid_{param}", str(values))

    # Lakukan pencarian grid pada data pelatihan
    grid_search.fit(X_train, y_train)

    print("\n--- Tuning Selesai ---")
    print(f"Parameter Terbaik: {grid_search.best_params_}")
    print(f"Skor Terbaik (F1-weighted pada CV): {grid_search.best_score_:.4f}")

    # Ambil model terbaik dari GridSearch
    best_model = grid_search.best_estimator_

    # Log parameter terbaik sebagai parameter run MLflow
    mlflow.log_params(grid_search.best_params_)

    # Prediksi pada X_val menggunakan model terbaik
    y_val_pred = best_model.predict(X_val)

    # Prediksi probabilitas untuk ROC AUC (pastikan model mendukung predict_proba)
    y_val_proba = None
    if hasattr(best_model, "predict_proba"):
        y_val_proba = best_model.predict_proba(X_val)[:, 1]

    # --- 4. Model Evaluation pada Data Validasi (Model Terbaik) ---
    val_accuracy = accuracy_score(y_val, y_val_pred)
    val_precision = precision_score(y_val, y_val_pred, average='weighted', zero_division=0)
    val_recall = recall_score(y_val, y_val_pred, average='weighted', zero_division=0)
    val_f1 = f1_score(y_val, y_val_pred, average='weighted', zero_division=0)

    # Log semua metrik evaluasi secara manual
    mlflow.log_metric("val_accuracy", val_accuracy)
    mlflow.log_metric("val_precision", val_precision)
    mlflow.log_metric("val_recall", val_recall)
    mlflow.log_metric("val_f1_score", val_f1)

    print(f"Akurasi Validasi (Model Terbaik): {val_accuracy:.4f}")
    print(f"Presisi Validasi (Model Terbaik): {val_precision:.4f}")
    print(f"Recall Validasi (Model Terbaik): {val_recall:.4f}")
    print(f"F1-Score Validasi (Model Terbaik): {val_f1:.4f}")

    if y_val_proba is not None:
        try:
            val_roc_auc = roc_auc_score(y_val, y_val_proba)
            print(f"ROC AUC Validasi (Model Terbaik): {val_roc_auc:.4f}")
            mlflow.log_metric("val_roc_auc_score", val_roc_auc)
        except ValueError as e:
            print(f"Tidak dapat menghitung ROC AUC untuk set validasi: {e}")

    # --- Tambahan Metrik untuk Manual Logging (minimal 2 nilai tambahan) ---
    # 1. Negative Predictive Value (NPV)
    tn, fp, fn, tp = confusion_matrix(y_val, y_val_pred).ravel()
    val_npv = tn / (tn + fn) if (tn + fn) != 0 else 0
    mlflow.log_metric("val_negative_predictive_value", val_npv)
    print(f"Negative Predictive Value Validasi: {val_npv:.4f}")

    # 2. Specificity (True Negative Rate)
    val_specificity = tn / (tn + fp) if (tn + fp) != 0 else 0
    mlflow.log_metric("val_specificity", val_specificity)
    print(f"Spesifisitas Validasi: {val_specificity:.4f}")

    # Catat confusion matrix sebagai artefak untuk set validasi
    cm = confusion_matrix(y_val, y_val_pred)
    cm_filename = f"confusion_matrix_val_{model_name.replace(' ', '_')}_best.csv"
    np.savetxt(cm_filename, cm, delimiter=",", fmt="%d")
    mlflow.log_artifact(cm_filename)
    print(f"Confusion Matrix untuk Model Terbaik disimpan sebagai artefak.")
    # Hapus file lokal setelah diunggah ke MLflow jika tidak lagi diperlukan
    if os.path.exists(cm_filename):
        os.remove(cm_filename)
        print(f"File lokal '{cm_filename}' dihapus.")

    # --- Mengatasi masalah `mlflow.sklearn.log_model` ---
    # Jika `mlflow.sklearn.log_model` menyebabkan masalah di DagsHub (seperti yang dilaporkan),
    # kita bisa menyimpan model secara manual dan mengunggahnya sebagai artefak umum.
    model_artifact_path = "best_random_forest_model.joblib"
    joblib.dump(best_model, model_artifact_path)
    mlflow.log_artifact(model_artifact_path, artifact_path="model")
    print(f"Model '{model_artifact_path}' logged as a general artifact.")

    # Hapus file lokal setelah diunggah
    if os.path.exists(model_artifact_path):
        os.remove(model_artifact_path)
        print(f"File lokal '{model_artifact_path}' dihapus.")

    # Tambahkan tag kustom
    mlflow.set_tag("Model Type", model_name)
    mlflow.set_tag("Dataset Split", "Train-Validation")
    mlflow.set_tag("Project", "Customer Churn Prediction")
    mlflow.set_tag("Tuning Result", "Best Model from GridSearchCV")

    print(f"MLflow Run ID: {mlflow.active_run().info.run_id}")

print("\nHyperparameter tuning dan pelatihan model terbaik selesai.")
print("Kunjungi DagsHub MLflow UI untuk melihat hasil dan membandingkan run ini.")