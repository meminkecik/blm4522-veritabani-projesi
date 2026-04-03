# Proje 2: Veritabanı Yedekleme ve Felaketten Kurtarma Planı

## 1. Tam Yedekleme (Full Backup) Alınması
Veritabanının mevcut durumunu güvence altına almak amacıyla PostgreSQL'in `pg_dump` aracı kullanılarak `dvdrental` veritabanının tam yedeği (Full Backup) oluşturulmuştur. 
Kullanılan komut:
`pg_dump -F c -d dvdrental -f dvdrental_tam_yedek.backup`

## 2. Felaket Senaryosu (Veri Kaybı Simülasyonu)
[cite_start]Sistemin kurtarma yeteneklerini test etmek için veritabanındaki en kritik tablolardan biri olan `payment` tablosu, ona bağlı olan görünümlerle (view) birlikte kasti olarak silinmiştir[cite: 35].
Kullanılan komut:
`DROP TABLE payment CASCADE;`
İşlem sonrasında `SELECT * FROM payment;` sorgusu çalıştırılmış ve tablonun veritabanından tamamen silindiği (relation does not exist hatası) teyit edilmiştir.

## 3. Felaketten Kurtarma (Restore)
[cite_start]Yaşanan veri kaybının ardından, sistemin ilk aşamada alınan yedek dosyası üzerinden kurtarılması işlemi başlatılmıştır[cite: 32]. [cite_start]Veritabanını yedeğin alındığı ana (point-in-time) temiz bir şekilde döndürmek için `--clean` parametresiyle restore işlemi gerçekleştirilmiştir[cite: 32].
Kullanılan komut:
`pg_restore -d dvdrental --clean --no-owner dvdrental_tam_yedek.backup`

[cite_start]Kurtarma işlemi sonrasında veritabanı kontrol edilmiş ve silinen `payment` tablosunun tüm verileriyle birlikte eksiksiz olarak geri yüklendiği doğrulanmıştır[cite: 35].
