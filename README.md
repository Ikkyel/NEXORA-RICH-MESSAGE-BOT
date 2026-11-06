# NEXORA RICH MESSAGE BOT

Telegram Mini App untuk menyusun, menyimpan, menjadwalkan, dan menerbitkan rich message ke **satu tujuan yang dipilih** setiap kali posting.

## Fitur yang disiapkan
- FastAPI backend dan Telegram bot polling sebagai dua proses terpisah.
- Validasi Telegram Mini App `initData` menggunakan HMAC-SHA256.
- PostgreSQL dengan SQLAlchemy; tabel dibuat otomatis saat aplikasi mulai.
- Draft tersimpan permanen sampai admin menghapusnya.
- Pesan teks, foto, video, parse mode HTML, dan inline URL buttons.
- Daftar tujuan Telegram; admin memilih satu tujuan per posting.
- Preview ringkas, posting langsung, dan jadwal posting.
- Riwayat sukses/gagal.
- Admin utama dapat menambah dan menghapus admin melalui API/panel.
- Mini App sederhana yang responsif.

## 1. Persiapan
1. Salin `.env.example` menjadi `.env`.
2. Isi `BOT_TOKEN`, `BOT_USERNAME`, `DATABASE_URL`, `WEBAPP_URL`, `APP_SECRET`, `ADMIN_IDS`, dan `PRIMARY_ADMIN_ID`.
3. Buat bot melalui @BotFather dan aktifkan menu button/Web App dengan URL HTTPS.
4. Tambahkan bot sebagai admin pada channel/grup tujuan dan berikan izin mengirim pesan.

`DATABASE_URL` harus memakai format SQLAlchemy psycopg, contoh:
`postgresql+psycopg://user:password@host:5432/database`
Jika password berisi karakter khusus URL, lakukan URL-encoding.

## 2. Instalasi Termux
```bash
pkg update && pkg upgrade -y
pkg install python git -y
python -m venv $HOME/nexora-venv
source $HOME/nexora-venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```
Edit `.env` memakai Acode atau nano.

## 3. Jalankan lokal
Terminal 1 (API + Mini App):
```bash
source $HOME/nexora-venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Terminal 2 (Telegram bot):
```bash
source $HOME/nexora-venv/bin/activate
python run_bot.py
```
Untuk pengujian Mini App di Telegram, backend harus tersedia melalui HTTPS publik dan `WEBAPP_URL` harus sama dengan URL Mini App.

## 4. Tambahkan tujuan
- Pastikan bot menjadi admin channel/grup.
- Buka Mini App sebagai admin.
- Masukkan Chat ID tujuan, misalnya `-1001234567890`, dan nama tujuan.
- Pilih tujuan tersebut saat membuat posting.

## 5. Catatan operasional
- Simpan `.env` secara privat dan jangan commit ke Git.
- `APP_SECRET` harus berupa nilai acak panjang, bukan token bot.
- Draft dan riwayat disimpan di database. Media Telegram disimpan sebagai `file_id`, bukan diunduh ke server.
- Scheduler berjalan di proses API. Pastikan hanya satu instance API aktif agar jadwal tidak dieksekusi ganda.
- Jadwal menggunakan waktu server; set `TZ`/zona server ke `Asia/Jakarta` bila diperlukan.
- Ini adalah baseline siap konfigurasi, tetap lakukan uji kirim ke channel privat sebelum produksi.
