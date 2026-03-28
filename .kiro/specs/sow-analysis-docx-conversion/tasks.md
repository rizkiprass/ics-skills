# Rencana Implementasi: SOW Analysis DOCX Conversion

## Ikhtisar

Implementasi skrip Python `convert_md_to_docx.py` untuk skill `cloud-sow-analyzer` yang mengonversi laporan analisis Markdown menjadi dokumen Word (.docx). Pendekatan: parse MD → struktur data intermediate (dataclasses) → build DOCX menggunakan `python-docx`. Setiap task membangun di atas task sebelumnya secara inkremental.

## Tasks

- [x] 1. Buat struktur file dan model data intermediate
  - [x] 1.1 Buat file `skills/cloud-sow-analyzer/scripts/convert_md_to_docx.py` dengan import, dataclass model (`TextRun`, `Paragraph`, `BulletItem`, `ChecklistItem`, `CodeBlock`, `Table`, `Section`), dan fungsi `main()` sebagai entry point CLI
    - Definisikan semua dataclass sesuai desain (field, default values, type hints)
    - Implementasikan `main()` dengan argparse: menerima `<input_md_file>` dan opsional `--output <output_docx_file>`
    - Tampilkan usage message jika argumen tidak valid
    - _Requirements: 5.1, 5.2, 5.3_

  - [x] 1.2 Tulis unit test untuk validasi CLI dan model data
    - Buat file `skills/cloud-sow-analyzer/scripts/test_convert_md_to_docx.py`
    - Test CLI tanpa argumen menampilkan usage message
    - Test dataclass instantiation dan default values
    - _Requirements: 5.3_


- [x] 2. Implementasi Markdown Parser
  - [x] 2.1 Implementasikan fungsi `parse_markdown(content: str) -> List[Section]`
    - Parse heading level 1-3 (`#`, `##`, `###`) menjadi `Section` dengan level yang sesuai
    - Parse tabel Markdown (header + separator + rows) menjadi `Table`
    - Parse bullet list (`- item`) menjadi `BulletItem` dengan dukungan nested level
    - Parse checklist (`- [ ]`, `- [x]`) menjadi `ChecklistItem`
    - Parse code block (triple backtick) menjadi `CodeBlock`
    - Parse inline formatting: `**bold**` dan `*italic*` menjadi `TextRun` dengan flag yang sesuai
    - Parse emoji indikator risiko (🔴, 🟠, 🟡, 🟢) menjadi `TextRun` dengan `is_risk_indicator=True`
    - Parse teks biasa menjadi `Paragraph` dengan `TextRun`
    - Parse horizontal rule (`---`) sebagai separator
    - _Requirements: 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4, 7.1, 7.2, 7.3_

  - [x] 2.2 Tulis property test untuk preservasi urutan section
    - **Property 3: Preservasi Urutan Section**
    - Generate random MD dengan multiple heading, verifikasi urutan heading di output sama dengan input
    - **Validates: Requirements 7.2**

  - [x] 2.3 Tulis property test untuk pemetaan hierarki heading
    - **Property 4: Pemetaan Hierarki Heading**
    - Generate random heading levels (1-3), verifikasi setiap heading dipetakan ke level yang benar
    - **Validates: Requirements 2.1**

  - [x] 2.4 Tulis property test untuk konversi tabel
    - **Property 5: Konversi Tabel dengan Fidelitas Data**
    - Generate random tabel (random cols/rows/data), verifikasi jumlah kolom, baris, dan data sel identik
    - **Validates: Requirements 2.2, 7.3**

  - [x] 2.5 Tulis unit test untuk parser dengan contoh spesifik
    - Test parsing heading H1, H2, H3
    - Test parsing tabel dengan emoji di dalam sel
    - Test parsing nested bullet list
    - Test parsing checklist checked dan unchecked
    - Test parsing code block
    - Test parsing bold dan italic inline
    - Test parsing file kosong
    - Test parsing file tanpa heading
    - _Requirements: 2.1, 2.3, 3.1, 3.2, 3.3, 3.4_

- [x] 3. Checkpoint - Pastikan parser berfungsi dengan benar
  - Pastikan semua test lulus, tanyakan ke user jika ada pertanyaan.


- [x] 4. Implementasi DOCX Builder
  - [x] 4.1 Implementasikan fungsi `build_docx(sections: List[Section], title: str) -> Document`
    - Konfigurasi dokumen: ukuran halaman US Letter, margin 1 inci semua sisi
    - Set font default Arial 11pt
    - Tambahkan header halaman dengan judul dokumen (rata kanan)
    - Tambahkan footer halaman dengan nomor halaman (rata tengah)
    - Render `Section` sebagai Heading Word (H1→Heading 1, H2→Heading 2, H3→Heading 3) dengan ukuran font sesuai desain (16pt, 14pt, 12pt)
    - Render `Table` sebagai tabel Word dengan border, header berwarna biru (#4472C4) teks putih bold, alternating row colors (#F2F2F2)
    - Render `BulletItem` sebagai bullet list Word terstruktur dengan dukungan level
    - Render `ChecklistItem` dengan prefix ☐ (unchecked) atau ☑ (checked)
    - Render `CodeBlock` dengan font Courier New 9pt dan background #F5F5F5
    - Render `Paragraph` dengan `TextRun` (bold, italic, risk indicator)
    - Render emoji risiko: pertahankan emoji asli, atau fallback ke teks berwarna ([CRITICAL], [HIGH], [MEDIUM], [LOW])
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 3.1, 3.2, 3.3, 3.4_

  - [x] 4.2 Tulis property test untuk preservasi emoji indikator risiko
    - **Property 6: Preservasi Emoji Indikator Risiko**
    - Generate random teks dengan emoji 🔴🟠🟡🟢, verifikasi representasi setara ada di DOCX
    - **Validates: Requirements 3.1**

  - [x] 4.3 Tulis property test untuk formatting inline dan list
    - **Property 7: Preservasi Formatting Inline dan List**
    - Generate random bold/italic/bullet/checklist, verifikasi formatting di DOCX
    - **Validates: Requirements 2.3, 3.2, 3.4**

  - [x] 4.4 Tulis property test untuk formatting code block
    - **Property 8: Formatting Code Block**
    - Generate random code block content, verifikasi font monospace di DOCX
    - **Validates: Requirements 3.3**

  - [x] 4.5 Tulis unit test untuk DOCX builder
    - Test heading styles (H1, H2, H3) memiliki level yang benar
    - Test tabel memiliki header berwarna dan alternating rows
    - Test checklist menggunakan prefix ☐/☑
    - Test code block menggunakan font Courier New
    - Test header dan footer halaman
    - Test margin dan ukuran halaman
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 3.1, 3.2, 3.3_


- [x] 5. Checkpoint - Pastikan builder DOCX berfungsi dengan benar
  - Pastikan semua test lulus, tanyakan ke user jika ada pertanyaan.

- [x] 6. Implementasi fungsi konversi utama dan error handling
  - [x] 6.1 Implementasikan fungsi `convert_md_to_docx(md_path: str, docx_path: str = None) -> tuple[bool, str]`
    - Cek import `python-docx`, tampilkan pesan error + instruksi instalasi jika tidak ada
    - Validasi file input ada, tampilkan pesan error dengan path jika tidak ditemukan
    - Derivasi path output: direktori sama, nama sama, ekstensi `.docx` (jika `docx_path` tidak diberikan)
    - Panggil `parse_markdown()` dan `build_docx()` secara berurutan
    - Tangkap semua exception, return `(False, pesan_error)` tanpa crash
    - Pastikan file MD sumber tidak dimodifikasi dalam kondisi apapun
    - Return `(True, pesan_sukses)` dengan path DOCX jika berhasil
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 4.1, 4.2, 4.3, 4.4_

  - [x] 6.2 Hubungkan `convert_md_to_docx()` ke `main()` CLI entry point
    - Panggil `convert_md_to_docx()` dari `main()` dengan argumen yang di-parse
    - Cetak pesan hasil (sukses/error) ke stdout
    - Return exit code 0 jika sukses, 1 jika gagal
    - _Requirements: 5.1, 5.2_

  - [x] 6.3 Tulis property test untuk derivasi path output
    - **Property 1: Derivasi Path Output**
    - Generate random filenames `.md` di random directories, verifikasi output path = same dir + same name + `.docx`
    - **Validates: Requirements 1.2, 1.3**

  - [x] 6.4 Tulis property test untuk kegagalan non-destruktif
    - **Property 9: Kegagalan Non-Destruktif**
    - Generate random MD, simulasi error (file corrupt, permission denied), verifikasi MD tidak berubah dan tidak ada unhandled exception
    - **Validates: Requirements 4.3, 4.4**

  - [x] 6.5 Tulis unit test untuk error handling
    - Test file tidak ditemukan menampilkan pesan error dengan path
    - Test dependency missing menampilkan instruksi instalasi
    - Test konversi gagal tidak mengubah file MD sumber
    - Test output path custom dengan `--output` flag
    - _Requirements: 4.1, 4.2, 4.3, 4.4_


- [x] 7. Integrasi end-to-end dan validasi dengan sample output
  - [x] 7.1 Jalankan konversi terhadap `examples/sample-analysis-output.md` dan validasi hasilnya
    - Konversi file sample, verifikasi DOCX valid dan bisa dibuka
    - Verifikasi semua section, tabel, checklist, emoji, code block terkonversi
    - Verifikasi header/footer halaman ada
    - Verifikasi font dan styling sesuai desain
    - _Requirements: 1.1, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 3.1, 3.2, 3.3, 3.4, 7.1, 7.2, 7.3_

  - [x] 7.2 Tulis property test untuk round-trip fidelitas konten
    - **Property 2: Round-Trip Fidelitas Konten**
    - Generate random MD dengan heading, teks, tabel, list; extract teks dari DOCX dan bandingkan dengan MD source
    - **Validates: Requirements 7.1**

  - [x] 7.3 Tulis integration test end-to-end
    - Test konversi sample-analysis-output.md menghasilkan DOCX valid
    - Test konversi file MD kosong tidak crash
    - Test konversi file tanpa heading tetap menghasilkan DOCX
    - Test tabel dengan kolom tidak rata
    - _Requirements: 7.1, 7.2, 7.3_


- [x] 8. Update dokumentasi workflow SOW Analyzer
  - [x] 8.1 Update `skills/cloud-sow-analyzer/SKILL.md` untuk menyertakan Phase 5B
    - Tambahkan deskripsi Phase 5B: Convert to DOCX antara Phase 5 dan Phase 6
    - Update pesan konfirmasi Phase 6 untuk menyertakan info DOCX
    - Update opsi "Export ke format lain" di Phase 6 untuk menginformasikan DOCX sudah tersedia
    - Tambahkan instruksi konversi manual: `python scripts/convert_md_to_docx.py <file.md>`
    - _Requirements: 6.1, 6.2, 6.3_

  - [x] 8.2 Update `skills/cloud-sow-analyzer/metadata.json`
    - Tambahkan `docx` ke `outputFormats`
    - Pastikan `python-docx` tetap di `requirements.optional`
    - _Requirements: 6.1_

- [x] 9. Final checkpoint - Pastikan semua test lulus
  - Pastikan semua test lulus, tanyakan ke user jika ada pertanyaan.

## Catatan

- Task bertanda `*` bersifat opsional dan bisa dilewati untuk MVP lebih cepat
- Setiap task mereferensikan persyaratan spesifik untuk traceability
- Checkpoint memastikan validasi inkremental
- Property test memvalidasi correctness properties universal dari desain
- Unit test memvalidasi contoh spesifik dan edge case
