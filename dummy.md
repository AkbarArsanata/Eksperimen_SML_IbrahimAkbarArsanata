Ah sip 👍 error itu muncul karena Mermaid **nggak boleh ada teks komentar (`%% ...`) setelah perintah node/link**.
Aku bersihin syntax-nya dan sederhanakan biar bisa langsung di-render.

Coba pakai versi berikut ini (sudah aku rapikan supaya valid):

```mermaid
flowchart LR
  %% ==== LANE / PERAN (sebagai subgraph) ====
  subgraph L0["No & Aktivitas"]
    A1["1. Perencanaan / Persiapan"]
    A2["2. Penyiapan & Matching Direktori Perusahaan IBS"]
    A3["3. Pencacahan"]
    A4["4. Pemeriksaan"]
    A5["5. Pengiriman Dokumen"]
  end

  subgraph L1["Kepala BPS Kab Rembang"]
    S0([MULAI])
    K1[Proses]
    D2{{Keputusan}}
    K4D{{Keputusan}}
    K5D{{Keputusan}}
  end

  subgraph L2["Ka Tim Statistik Produksi"]
    KT1[Proses]
    KT2[Proses]
    KT3[Proses]
    KT4[Proses]
    KT5[Proses]
  end

  subgraph L3["Anggota Tim Statistik Produksi"]
    AT1[Proses]
    AT2[Proses]
    AT3[Proses]
    AT4[Proses]
    AT5[Proses]
  end

  subgraph L4["Kasubbag Umum"]
    KU1[Proses]
    KU2[Proses]
    KU3[Proses]
    KU4[Proses]
    KU5[Proses]
  end

  subgraph L5["Staf Subbag Umum"]
    SU1[Proses]
    SU2[Proses]
    SU3[Proses]
    SU4[Proses]
    SU5[Proses]
  end

  subgraph L6["PJ Kec / Mitra"]
    PJ1[Proses]
    PJ2[Proses]
    PJ3[Proses]
    PJ4[Proses]
    PJ5[Proses]
  end

  subgraph L7["BPS Prov Jateng"]
    BP1[Proses]
    BP2[Proses]
    BP3[Proses]
    BP4[Proses]
    BP5[/Dokumen diterima/]
    END0([SELESAI])
  end

  %% ==== ALUR KEGIATAN 1 ====
  S0 --> K1 --> KT1 --> AT1 --> KU1 --> SU1 --> PJ1 --> BP1

  %% ==== ALUR KEGIATAN 2 ====
  A2 --- D2
  D2 -->|Y| KT2 --> AT2 --> SU2 --> PJ2 --> BP2
  D2 -->|T| K1

  %% ==== ALUR KEGIATAN 3 ====
  A3 --- KT3 --> AT3 --> PJ3 --> BP3
  AT3 --> KU3 --> SU3 --> PJ3

  %% ==== ALUR KEGIATAN 4 ====
  A4 --- K4D
  K4D -->|Y| AT4 --> KT4 --> SU4 --> PJ4 --> BP4
  K4D -->|T| K4D

  %% ==== ALUR KEGIATAN 5 ====
  A5 --- K5D
  K5D -->|Y| KT5 --> AT5 --> KU5 --> SU5 --> PJ5 --> BP5 --> END0
  K5D -->|T| K5D
```

⚡ Coba render lagi di [Mermaid Live Editor](https://mermaid.live).
Kalau sukses, aku bisa lanjut tambahkan isi detail “Mutu Baku” (persyaratan, waktu, output) ke flowchart ini juga biar tabel kanan ikut divisualkan.

Mau aku tambahkan langsung juga bagian “Mutu Baku”-nya ke dalam diagram atau dijadikan tabel terpisah biar lebih rapi?
