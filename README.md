MEMETRIXA — Solana Risk Scanner

MEMETRIXA adalah proyek Python untuk mengambil data pasar token Solana dan melakukan penilaian risiko awal berdasarkan indikator seperti likuiditas, volume transaksi, umur trading pair, dan aktivitas jual-beli.

Versi: 0.1.0
Bahasa: Python
Sumber data pasar: DexScreener API

Fitur

Mengambil data trading pair token Solana.

Menampilkan nama dan simbol token.

Menampilkan likuiditas dan volume 24 jam.

Menghitung skor risiko awal dari 0–100.

Menampilkan kategori risiko dan indikator peringatan.

Persyaratan

Python 3

Git (jika ingin mengunduh melalui GitHub)

Koneksi internet

Instalasi

1. Unduh repository

Setelah repository tersedia di GitHub, jalankan:

git clone URL_REPOSITORY_KAMU
cd MEMETRIXA

Ganti URL_REPOSITORY_KAMU dengan URL repository milikmu.

2. Buat virtual environment (disarankan)

python3 -m venv .venv
source .venv/bin/activate

Jika perintah python3 -m venv .venv gagal di Ubuntu/WSL, pasang paket python3-venv melalui pengelola paket sistem terlebih dahulu.

3. Instal dependensi

python -m pip install -r requirements.txt

4. Jalankan aplikasi

python main.py

Masukkan alamat mint token Solana ketika diminta.

Untuk pengujian, gunakan alamat Wrapped SOL:

So11111111111111111111111111111111111111112

Aplikasi akan menampilkan data pasar dan hasil penilaian risiko yang tersedia.

Cara Membaca Hasil

Likuiditas: perkiraan nilai likuiditas trading pair dalam USD.

Volume 24h: volume perdagangan selama 24 jam.

Skor Risiko: skor heuristik awal, bukan probabilitas scam.

Kategori: klasifikasi berdasarkan aturan skor pada kode.

Peringatan: indikator yang memerlukan pemeriksaan lebih lanjut.

Memperbarui Kode

Buka proyek di VS Code.

Edit file yang ingin diperbarui.

Simpan perubahan.

Jalankan kembali python main.py.

Uji hasilnya sebelum membagikan versi baru.

Batasan

MEMETRIXA saat ini menggunakan aturan penilaian risiko sederhana dan data pasar yang tersedia dari DexScreener. Versi ini belum dapat memastikan token merupakan scam, honeypot, atau rug pull. Skor rendah bukan jaminan keamanan.

Lakukan pemeriksaan tambahan sebelum mengambil keputusan investasi.

Lisensi

Belum ditentukan. Tambahkan file lisensi jika ingin menetapkan ketentuan penggunaan dan distribusi proyek.MEMETRIXA — Solana Risk Scanner

MEMETRIXA adalah proyek Python untuk mengambil data pasar token Solana dan melakukan penilaian risiko awal berdasarkan indikator seperti likuiditas, volume transaksi, umur trading pair, dan aktivitas jual-beli.

Versi: 0.1.0
Bahasa: Python
Sumber data pasar: DexScreener API

Fitur

Mengambil data trading pair token Solana.

Menampilkan nama dan simbol token.

Menampilkan likuiditas dan volume 24 jam.

Menghitung skor risiko awal dari 0–100.

Menampilkan kategori risiko dan indikator peringatan.

Persyaratan

Python 3

Git (jika ingin mengunduh melalui GitHub)

Koneksi internet

Instalasi

1. Unduh repository

Setelah repository tersedia di GitHub, jalankan:

git clone URL_REPOSITORY_KAMU
cd MEMETRIXA

Ganti URL_REPOSITORY_KAMU dengan URL repository milikmu.

2. Buat virtual environment (disarankan)

python3 -m venv .venv
source .venv/bin/activate

Jika perintah python3 -m venv .venv gagal di Ubuntu/WSL, pasang paket python3-venv melalui pengelola paket sistem terlebih dahulu.

3. Instal dependensi

python -m pip install -r requirements.txt

4. Jalankan aplikasi

python main.py

Masukkan alamat mint token Solana ketika diminta.

Untuk pengujian, gunakan alamat Wrapped SOL:

So11111111111111111111111111111111111111112

Aplikasi akan menampilkan data pasar dan hasil penilaian risiko yang tersedia.

Cara Membaca Hasil

Likuiditas: perkiraan nilai likuiditas trading pair dalam USD.

Volume 24h: volume perdagangan selama 24 jam.

Skor Risiko: skor heuristik awal, bukan probabilitas scam.

Kategori: klasifikasi berdasarkan aturan skor pada kode.

Peringatan: indikator yang memerlukan pemeriksaan lebih lanjut.

Memperbarui Kode

Buka proyek di VS Code.

Edit file yang ingin diperbarui.

Simpan perubahan.

Jalankan kembali python main.py.

Uji hasilnya sebelum membagikan versi baru.

Batasan

MEMETRIXA saat ini menggunakan aturan penilaian risiko sederhana dan data pasar yang tersedia dari DexScreener. Versi ini belum dapat memastikan token merupakan scam, honeypot, atau rug pull. Skor rendah bukan jaminan keamanan.

Lakukan pemeriksaan tambahan sebelum mengambil keputusan investasi.

Lisensi

Belum ditentukan. Tambahkan file lisensi jika ingin menetapkan ketentuan penggunaan dan distribusi proyek.
