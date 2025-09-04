Makasih fotonya! Aku udah bikin ulang flowchart-nya dalam Mermaid. Beberapa teks kecil di tabel “Mutu Baku” dan label dalam kotak proses kurang terbaca di foto, jadi aku salin yang terlihat jelas dan sisakan placeholder pada bagian yang tak terbaca (pakai tanda `[??]`). Kamu bisa tempel kode ini ke editor Mermaid (mis. mermaid.live) lalu kita iterasi kalau mau aku lengkapi dari foto yang lebih jelas.

```mermaid
flowchart LR
  %% ==== LANE / PERAN (sebagai subgraph) ====
  subgraph L0["No & Aktivitas"]
    A1["1. Perencanaan / Persiapan"]
    A2["2. Penyiapan & Matching Direktori Perusahaan Industri Besar Sedang"]
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
  D2 -->|T| K1  %% kembali ke proses sebelumnya (panah balik terlihat di gambar)

  %% ==== ALUR KEGIATAN 3 ====
  A3 --- KT3 --> AT3 --> PJ3 --> BP3
  AT3 --> KU3
  KU3 --> SU3
  SU3 -->|T| PJ3

  %% ==== ALUR KEGIATAN 4 (ada keputusan) ====
  A4 --- K4D
  K4D -->|Y| AT4 --> KT4 --> SU4 --> PJ4 --> BP4
  K4D -->|T| K4D  %% loop pemeriksaan ulang (tampak ada panah balik)

  %% ==== ALUR KEGIATAN 5 (pengiriman dokumen) ====
  A5 --- K5D
  K5D -->|Y| KT5 --> AT5 --> KU5 --> SU5 --> PJ5 --> BP5 --> END0
  K5D -->|T| K5D

  %% ==== MUTU BAKU (ringkasan di kolom kanan tabel) ====
  subgraph MB["Mutu Baku"]
    MB1P["Kegiatan 1 - Persyaratan/Kelengkapan: POK, DIPA/DPA BPS, Dokumen Surat, ATK"]
    MB1W["Waktu: 7 hari (Desember t-1 / Januari t)"]
    MB1O["Output: Rencana anggaran kegiatan & kelengkapan administrasi"]
    MB2P["Kegiatan 2 - Persyaratan/Kelengkapan: Surat Tugas, Surat Pengantar Pengambilan Direktori, Daftar IKB, ATK"]
    MB2W["Waktu: 1 bulan (Januari–Februari)"]
    MB2O["Output: Direktori Perusahaan IBS [??]"]
    MB3P["Kegiatan 3 - Persyaratan/Kelengkapan: Daftar IA, IB, I, B & ATK; Surat Tugas"]
    MB3W["Waktu: 1 bulan (Februari–Juni)"]
    MB3O["Output: Daftar IB baru atau [??]"]
    MB4P["Kegiatan 4 - Persyaratan/Kelengkapan: Daftar IA dan/atau IB lama; ATK; Surat Tugas"]
    MB4W["Waktu: 1 bulan (Mei–Juli)"]
    MB4O["Output: Daftar IA dan/atau IB lama terisi lengkap [??]"]
    MB5P["Kegiatan 5 - Persyaratan/Kelengkapan: Daftar IA dan/atau IB lama/baru siap kirim"]
    MB5W["Waktu: 2 hari (Mei–Juli)"]
    MB5O["Output: Daftar IA dan/atau IB [??] terkirim"]
  end
```

Kalau kamu punya foto yang sedikit lebih tajam (atau versi PDF), kirim aja—nanti aku perbarui bagian `[??]` dan arah panah yang spesifik supaya benar-benar “persis” 1:1 dengan dokumenmu.
