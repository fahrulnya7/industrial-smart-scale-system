# industrial-smart-scale-system
IoT-Based Industrial Batching &amp; Labeling System with Centralized Data Management
1. Enjoy with cofee,
2. Penjelasan Sistem & Alur Kerja
   Konsep: Sistem ini menggunakan arsitektur Client-Server.

    2A.  Server (Ubuntu di Proxmox): Bertindak sebagai "Otak Pusat". Menyimpan database, melayani halaman Admin (Master Data, Hasil, Setting Operator),           dan menerima data kiriman dari produksi.

    2B.  Client (Raspberry Pi): Bertindak sebagai "Station". Terhubung langsung ke Timbangan dan Printer. Menjalankan tampilan khusus operator,         
          memproses logika LOT Number, dan mengirim hasil kerja ke Server Pusat.

3. Topologi Jaringan:

[Timbangan Digital] --(RS232 USB)--> [Raspberry Pi 4] --(USB)--> [Printer Zebra]
                                            |
                                       (LAN / WiFi)
                                            |
                                     [Router / Switch]
                                            |
[PC Admin/Office] ------------------ [Server Ubuntu (Proxmox)]
(Akses Dashboard via Browser)


4. Flowchart Alur Data:

  4.1. Admin upload CSV "Master Data Product" ke Server.
  4.2. Admin setting nama Operator, Mesin, Shift di Server.
  4.3. Raspberry Pi menyala -> Download data update dari Server.
  4.4. Operator di Pi scan/pilih Product -> Data Timbangan masuk otomatis.
  4.5. Sistem Pi generate "LOT Number" otomatis berdasarkan logika (Tanggal, Shift, Kode Material, Counter).
  4.6. Operator tekan Print -> Sticker keluar -> Data dikirim ke Server (Halaman Hasil).
  4.7. Server update "Jumlah Terproduksi" di database pusat.

5. Persiapan Keamanan (Wajib Dilakukan Pertama)
Agar sistem aman, ganti password pada bagian berikut:
  5.1.  Ubuntu Server (Proxmox):
        User root atau user default saat instalasi.
        Command: passwd
  5.2.  Raspberry Pi:
        User default pi.
        Command: passwd
  5.3.  Database & Login Web:
        Nanti di dalam script konfigurasi (config.py), pastikan mengganti SECRET_KEY dan password admin default.

6. Struktur Folder GitHub
industrial-smart-scale-system/
├── server/                   <-- DIUPLOAD KE PROXMOX
│   ├── app.py                (Main Server Logic)
│   ├── requirements.txt
│   ├── database.db           (SQLite auto-created)
│   ├── static/               (CSS/JS)
│   ├── templates/            (HTML Admin/Hasil/Setting)
│   └── install_server.sh     (One-Click Installer Server)
├── station/                  <-- DIUPLOAD KE RASPBERRY PI
│   ├── main_station.py       (Logic Timbangan & Printer)
│   ├── requirements.txt
│   ├── templates/            (HTML Layar Station Kiri/Kanan)
│   └── install_pi.sh         (One-Click Installer Pi)
├── docs/
│   ├── topology.png
│   ├── manual.pdf
│   └── master_data_sample.csv
└── README.md
