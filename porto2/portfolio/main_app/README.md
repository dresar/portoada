# Portfolio Website - Dummy Data

File-file ini berisi data dummy dan script untuk mengimpor data ke dalam database Django untuk website portfolio.

## Struktur File

- `dummy_data.json` - File JSON yang berisi data dummy untuk semua model dalam aplikasi
- `import_dummy_data.py` - Script Python untuk mengimpor data dummy ke dalam database Django

## Cara Menggunakan

### 1. Persiapan

Pastikan Django project sudah disetup dengan benar dan database sudah dikonfigurasi. Semua model yang diperlukan sudah harus dibuat dan migrasi sudah dijalankan.

### 2. Mengimpor Data Dummy

Untuk mengimpor data dummy ke dalam database, jalankan perintah berikut dari direktori yang sama dengan file `import_dummy_data.py`:

```bash
python import_dummy_data.py
```

Atau jika Anda menggunakan Django shell:

```bash
python manage.py shell
```

Kemudian di dalam shell:

```python
exec(open('main_app/import_dummy_data.py').read())
```

### 3. Catatan Penting

- Script ini akan membuat placeholder image untuk semua field gambar. Untuk hasil yang lebih baik, Anda sebaiknya mengganti gambar-gambar ini dengan gambar yang sebenarnya.
- Secara default, script tidak akan menghapus data yang sudah ada. Jika Anda ingin menghapus data yang sudah ada sebelum mengimpor data baru, Anda dapat menghapus komentar pada bagian "Clear existing data" di dalam script.
- Pastikan Anda memiliki library Pillow terinstall untuk pembuatan placeholder image:
  ```bash
  pip install Pillow
  ```

## Kustomisasi Data

Anda dapat menyesuaikan data dummy dengan mengedit file `dummy_data.json`. Struktur file ini mengikuti model-model yang ada dalam aplikasi Django.

## Model yang Didukung

Script ini mendukung pengimporan data untuk model-model berikut:

1. PersonalInfo - Informasi pribadi
2. SocialMedia - Media sosial
3. Education - Pendidikan
4. SkillCategory - Kategori skill
5. Skill - Skill
6. ProjectCategory - Kategori project
7. Project - Project
8. ProjectImage - Gambar project
9. Experience - Pengalaman kerja
10. Certificate - Sertifikat
11. Service - Layanan
12. Testimonial - Testimonial
13. BlogCategory - Kategori blog
14. BlogPost - Artikel blog

## Troubleshooting

Jika Anda mengalami masalah saat menjalankan script:

1. Pastikan semua dependensi terinstall
2. Periksa apakah struktur model Anda sesuai dengan yang diharapkan oleh script
3. Periksa apakah database Anda sudah dimigrasi dengan benar
4. Jika ada error spesifik, periksa pesan error untuk informasi lebih lanjut