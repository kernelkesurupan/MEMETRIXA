<div align="center">

# MEMETRIXA

**Solana Token Risk Scanner**

Cek risiko token Solana sebelum kamu beli, langsung dari terminal.

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![Version](https://img.shields.io/badge/version-2.0-8A2BE2)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
![Data](https://img.shields.io/badge/data-DexScreener-00C2FF)
![Chain](https://img.shields.io/badge/chain-Solana-14F195?logoColor=black)

by **kernelkesurupan**

</div>

---

## Apa ini?

Memetrixa mengambil data pasar token Solana dari DexScreener, lalu mengecek beberapa hal di blockchain (mint authority, freeze authority, sebaran holder). Hasilnya dijadikan skor risiko 0–100 plus daftar peringatan, jadi kamu tahu apa saja yang perlu dicurigai.

Ini alat bantu untuk riset awal, bukan penentu token itu scam atau bukan.

## Fitur

| | |
|---|---|
| 📊 **Data pasar** | Harga, likuiditas, volume 24 jam, FDV, umur pair, transaksi beli/jual |
| 🔐 **Cek on-chain** | Mint authority, freeze authority, konsentrasi top holder |
| 🎯 **Skor risiko** | 0–100 dengan 4 kategori: Rendah, Sedang, Tinggi, Sangat Tinggi |
| ⚠️ **Peringatan** | Alasan skor dijelaskan satu per satu, bukan angka mentah |
| 🖥️ **Tampilan rapi** | Kotak berwarna dan bar skor di terminal |
| 💾 **Export JSON** | Simpan hasil scan untuk diolah lagi |
| 🛡️ **Aman** | Menolak input private key / seed phrase, HTTPS only, tanpa dependensi |

## Contoh tampilan

```
╔══════════════════════════════════════════════════════════════╗
║ TestCoin (TST)   pair 1/1                                    ║
╠══════════════════════════════════════════════════════════════╣
║ Mint        : So111111…11111112                              ║
║ DEX         : raydium                                        ║
║ Likuiditas  : $3,200.00                                      ║
║ Volume 24h  : $90,000.00                                     ║
║ Umur pair   : 30 menit                                       ║
║ Mint auth   : AKTIF                                          ║
╠══════════════════════════════════════════════════════════════╣
║ SKOR RISIKO 100/100  SANGAT TINGGI                           ║
║ ██████████████████████████████                               ║
╠══════════════════════════════════════════════════════════════╣
║ PERINGATAN                                                   ║
║ ▲ Likuiditas rendah (<$5K)                                   ║
║ ▲ Pair baru dibuat (<1 jam)                                  ║
║ ▲ Mint authority AKTIF: dev bisa mencetak token tanpa batas  ║
╚══════════════════════════════════════════════════════════════╝
```

*(Data di atas hanya contoh. Di terminal aslinya berwarna.)*

## Instalasi

Kamu cuma butuh **Python 3.8+** dan koneksi internet. Tidak ada paket tambahan yang perlu diinstal.

```bash
git clone URL_REPOSITORY_KAMU
cd MEMETRIXA
python3 main.py
```

Ganti `URL_REPOSITORY_KAMU` dengan URL repo milikmu.

## Cara pakai

**Mode interaktif**, tempel alamat mint token lalu Enter. Ketik `q` untuk keluar:

```bash
python3 main.py
```

**Langsung scan satu token:**

```bash
python3 main.py So11111111111111111111111111111111111111112
```

Alamat di atas adalah Wrapped SOL, cocok buat coba-coba.

### Opsi

| Opsi | Fungsi |
|---|---|
| `--top N` | Jumlah pair teratas yang dianalisis, 1–10 (default 3) |
| `--json FILE` | Simpan hasil ke file JSON |
| `--no-onchain` | Lewati pengecekan on-chain (lebih cepat) |
| `--no-color` | Matikan warna |

Contoh:

```bash
python3 main.py <MINT_ADDRESS> --top 5 --json hasil.json
```

### RPC sendiri (opsional)

RPC publik Solana gratis tapi sering kena rate limit. Kalau punya RPC sendiri (harus HTTPS):

```bash
export MEMETRIXA_RPC="https://rpc-kamu.example.com"
```

## Cara membaca hasil

| Skor | Kategori | Artinya |
|---|---|---|
| 0–19 | 🟢 Rendah | Tidak ada tanda bahaya besar dari pengecekan dasar |
| 20–39 | 🟡 Sedang | Ada beberapa hal yang perlu dicek |
| 40–59 | 🔴 Tinggi | Banyak indikator berisiko |
| 60–100 | 🔴 Sangat Tinggi | Hati-hati sekali |

Yang dinilai: likuiditas, umur pair, volume dan jumlah transaksi, pergerakan harga, rasio FDV terhadap likuiditas, kelengkapan website/sosmed, status authority token, dan konsentrasi holder.

**Skor makin tinggi = makin berisiko.** Ini skor heuristik dari aturan sederhana, bukan probabilitas scam.

## Struktur proyek

```
memetrixa/
├── main.py                  # entry point + CLI
└── app/
    ├── ui.py                # tampilan terminal
    └── scanner/
        ├── market_data.py   # ambil data DexScreener
        ├── onchain.py       # cek authority & holder via RPC
        ├── risk_scanner.py  # hitung skor risiko
        └── net.py           # HTTP client aman
```

Mau ubah bobot skor? Buka `app/scanner/risk_scanner.py`, semua aturannya ada di fungsi `analyze_pair`.

## Keamanan

- Memetrixa **tidak pernah** meminta private key atau seed phrase. Kalau kamu tidak sengaja memasukkannya, input langsung ditolak dan tidak disimpan.
- Hanya koneksi HTTPS, dengan timeout dan batas ukuran respons.
- Nama token dari API dibersihkan dari karakter kontrol sebelum ditampilkan.

## Batasan

- Belum bisa mendeteksi **honeypot** atau status **LP lock**.
- Persentase holder bisa ikut menghitung akun pool likuiditas, jadi kadang terlihat lebih tinggi dari aslinya.
- Data tergantung DexScreener dan RPC publik. Kalau salah satunya error, hasil bisa kurang lengkap.
- Skor rendah **bukan** jaminan aman.

> ⚠️ **Disclaimer:** Ini bukan saran finansial. Selalu riset sendiri (DYOR) sebelum membeli token apa pun.

## Lisensi

Belum ditentukan. Tambahkan file `LICENSE` kalau mau menetapkan aturan pakai dan distribusi.

---

<div align="center">

Dibuat oleh **kernelkesurupan**

</div>
