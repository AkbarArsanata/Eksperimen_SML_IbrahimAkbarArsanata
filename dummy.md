```mermaid
flowchart TB
    A["Ambil Data<br/>(Google Sheet CSV,<br/>Data Cleaning,<br/>Validasi, Distribusi)"]
    B["OCR<br/>(Konversi PDF ke Teks,<br/>Tesseract, CNN+LSTM)"]
    C["Klasifikasi Dokumen<br/>(Preprocessing,<br/>LLM Gemini,<br/>Evaluasi & Integrasi BigQuery)"]
    D["Named Entity Recognition (NER)<br/>(Ekstraksi Tanggal, Waktu,<br/>Lokasi, Stakeholders)"]
    E["Integrasi ke Google Calendar<br/>(Validasi, Format ISO 8601,<br/>Penjadwalan & API)"]
    F["Vector Embeddings<br/>(TF-IDF → Embedding,<br/>Cosine Similarity)"]
    G["Matching Engine<br/>(ANN Search,<br/>Ranking, Evaluasi)"]
    H["Integrasi LLM Gemini<br/>(RAG, Prompt Engineering,<br/>Jawaban Kontekstual)"]

    %% Alur utama
    A --> B --> C --> D --> E

    %% Cabang dari preprocessing (sebelum klasifikasi final)
    C -. "Pasca Preprocessing" .-> F --> G --> H
