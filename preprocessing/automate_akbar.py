import pandas as pd
from scipy.stats.mstats import winsorize
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import os

def automate_data_preprocessing(df: pd.DataFrame, target_column: str, test_size: float = 0.20, random_state: int = 42) -> tuple:
    """
    Mengotomatiskan proses data preprocessing termasuk One-Hot Encoding,
    pengubahan tipe data, Winsorizing, penghapusan kolom,
    train-test split, Standard Scaling, dan SMOTE.

    Args:
        df (pd.DataFrame): DataFrame input yang akan diproses.
        target_column (str): Nama kolom target (variabel dependen).
        test_size (float): Proporsi dataset untuk dipecah sebagai data uji. Default 0.20.
        random_state (int): Seed untuk random_state untuk reproduktifitas. Default 42.

    Returns:
        tuple: Mengembalikan X_train_smote, X_test, y_train_smote, y_test
                setelah semua proses preprocessing.
    """

    # --- 1. One-Hot Encoding ---
    categorical_cols = ['Gender', 'Geography']
    df_encoded = pd.get_dummies(df.copy(), columns=categorical_cols, drop_first=True)
    print("--- One-Hot Encoding Selesai ---")
    print(df_encoded.head())
    print("\nKolom-kolom baru setelah encoding:", [col for col in df_encoded.columns if any(cat_col in col for cat_col in categorical_cols)])
    print("-" * 50)

    # --- 2. Mengubah Tipe Data Kolom One-Hot Encoded ke Integer ---
    newly_encoded_cols = [col for col in df_encoded.columns if any(cat_col + '_' in col for cat_col in categorical_cols)]
    for col in newly_encoded_cols:
        df_encoded[col] = df_encoded[col].astype(int)
    print("\n--- Kolom One-Hot Encoded diubah ke int ---")
    print(df_encoded[newly_encoded_cols].head())
    print("-" * 50)

    # --- 3. Winsorizing Outlier ---
    columns_to_winsorize = ['CreditScore', 'Age']
    lower_limit_percentile = 0.05
    upper_limit_percentile = 0.05

    print(f"\n--- Sebelum Winsorizing pada {columns_to_winsorize} ---")
    print(df_encoded[columns_to_winsorize].describe())

    for col in columns_to_winsorize:
        df_encoded[col] = winsorize(df_encoded[col], limits=[lower_limit_percentile, upper_limit_percentile], axis=0)

    print(f"\n--- Setelah Winsorizing pada {columns_to_winsorize} ---")
    print(df_encoded[columns_to_winsorize].describe())
    print("-" * 50)

    # --- 4. Penghapusan Kolom yang Tidak Diperlukan ---
    columns_to_drop = ['RowNumber', 'CustomerId', 'Surname']
    columns_to_drop_existing = [col for col in columns_to_drop if col in df_encoded.columns]
    df_cleaned = df_encoded.drop(columns=columns_to_drop_existing)
    print("\n--- Kolom yang tidak diperlukan dihapus ---")
    print(f"Kolom yang dihapus: {columns_to_drop_existing}")
    print(f"Jumlah kolom setelah penghapusan: {df_cleaned.shape[1]}")
    print("-" * 50)

    # --- 5. Train-Test Split ---
    X = df_cleaned.drop(target_column, axis=1)
    y = df_cleaned[target_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    print("\n--- Train-Test Split Selesai ---")
    print(f"Jumlah data training fitur (X_train): {X_train.shape[0]} baris")
    print(f"Jumlah data testing fitur (X_test): {X_test.shape[0]} baris")
    print(f"Jumlah data training target (y_train): {y_train.shape[0]} baris")
    print(f"Jumlah data testing target (y_test): {y_test.shape[0]} baris")
    print("-" * 50)

    # --- 6. Standard Scaling ---
    features_to_scale = [
        'CreditScore', 'Age', 'Balance', 'NumOfProducts', 'EstimatedSalary',
        'Tenure' # Menambahkan 'Tenure' di sini
    ]
    if 'BalanceToSalaryRatio' in X_train.columns:
        features_to_scale.append('BalanceToSalaryRatio')

    features_to_scale_existing = [col for col in features_to_scale if col in X_train.columns]

    scaler = StandardScaler()
    X_train[features_to_scale_existing] = scaler.fit_transform(X_train[features_to_scale_existing])
    X_test[features_to_scale_existing] = scaler.transform(X_test[features_to_scale_existing])

    print("\n--- Standard Scaling Selesai ---")
    print("Fitur-fitur di X_train setelah scaling:")
    print(X_train[features_to_scale_existing].head())
    print("\nFitur-fitur di X_test setelah scaling:")
    print(X_test[features_to_scale_existing].head())
    print("-" * 50)

    # --- 7. SMOTE untuk Penanganan Imbalance Data ---
    smote = SMOTE(random_state=random_state)
    X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

    print("\n--- SMOTE Selesai ---")
    print(f"Jumlah sampel di X_train sebelum SMOTE: {X_train.shape[0]} baris")
    print(f"Jumlah sampel di y_train sebelum SMOTE:")
    print(y_train.value_counts())
    print(f"\nJumlah sampel di X_train_smote setelah SMOTE: {X_train_smote.shape[0]} baris")
    print(f"Jumlah sampel di y_train_smote setelah SMOTE:")
    print(y_train_smote.value_counts())
    print("-" * 50)

    return X_train_smote, X_test, y_train_smote, y_test

# --- Cara Penggunaan ---
df = pd.read_csv('../Churn_Modelling.csv')

# Panggil fungsi otomatisasi preprocessing
X_train_processed, X_test_processed, y_train_processed, y_test_processed = automate_data_preprocessing(df.copy(), target_column='Exited')

print("\n--- Preprocessing Selesai dan Data Siap untuk Model ---")
print(f"Bentuk X_train_processed: {X_train_processed.shape}")
print(f"Bentuk X_test_processed: {X_test_processed.shape}")
print(f"Bentuk y_train_processed: {y_train_processed.shape}")
print(f"Bentuk y_test_processed: {y_test_processed.shape}")

# --- Menyimpan File Output ke CSV ---
current_directory = os.getcwd()
print(f"\nMenyimpan output di direktori: {current_directory}")

# Gabungkan X_train_smote dan y_train_smote
df_train_final = pd.concat([X_train_processed, y_train_processed], axis=1)
df_train_final.to_csv(os.path.join(current_directory, 'churn_train_preprocessed.csv'), index=False)
print("File 'churn_train_preprocessed.csv' berhasil disimpan.")

# Gabungkan X_test dan y_test
df_test_final = pd.concat([X_test_processed, y_test_processed], axis=1)
df_test_final.to_csv(os.path.join(current_directory, 'churn_test_preprocessed.csv'), index=False)
print("File 'churn_test_preprocessed.csv' berhasil disimpan.")
