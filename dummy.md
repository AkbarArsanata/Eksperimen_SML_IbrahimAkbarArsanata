```mermaid
flowchart TB
    %% Tahap awal
    A["Ambil Data<br/>(Google Sheet CSV,<br/>Data Cleaning,<br/>Validasi, Distribusi)"]
    B["OCR<br/>(Konversi PDF ke Teks,<br/>Tesseract, CNN+LSTM)"]

    %% Klasifikasi dipisah jadi dua tahap
    C1["Preprocessing Teks<br/>(Tokenisasi, Stopword Removal,<br/>Stemming, Vectorisasi)"]
    C2["Klasifikasi Dokumen<br/>(LLM Gemini,<br/>Evaluasi & Integrasi BigQuery)"]

    %% Jalur utama
    D["Named Entity Recognition (NER)<br/>(Ekstraksi Tanggal, Waktu,<br/>Lokasi, Stakeholders)"]
    E["Integrasi ke Google Calendar<br/>(Validasi, Format ISO 8601,<br/>Penjadwalan & API)"]

    %% Jalur percabangan Embeddings
    F["Vector Embeddings<br/>(Word2Vec/BERT,<br/>Cosine Similarity)"]
    G["Matching Engine<br/>(Approximate Nearest Neighbor Search,<br/>Ranking & Evaluasi)"]
    H["Integrasi LLM Gemini<br/>(Retrieval-Augmented Generation,<br/>Prompt Engineering)"]

    %% Alur utama
    A --> B --> C1 --> C2 --> D --> E

    %% Cabang dari preprocessing ke embeddings
    C1 --> F --> G --> H
