# Proje 1: Veritabanı Performans Optimizasyonu ve İzleme

## 1. Veritabanı Kurulumu
Projede kullanılmak üzere PostgreSQL için açık kaynaklı "DVD Rental" örnek veritabanı seçildi. Veritabanı `pg_restore` aracı kullanılarak terminal üzerinden sisteme başarıyla içeri aktarıldı. 15 adet tablo (actor, film, customer vb.) sisteme tanımlandı.

## 2. İzleme (Monitoring) Altyapısının Kurulumu
Sorgu performanslarını izleyebilmek, execution time'ları görmek ve yavaş çalışan sorguları tespit edebilmek amacıyla PostgreSQL'in `pg_stat_statements` eklentisi yapılandırıldı.

Bu işlem için `postgresql.conf` dosyası üzerinde aşağıdaki değişiklik yapıldı:
`shared_preload_libraries = 'pg_stat_statements'`

Ardından PostgreSQL servisi yeniden başlatıldı ve dvdrental veritabanı içerisinde eklenti aktif edildi:
`CREATE EXTENSION IF NOT EXISTS pg_stat_statements;`

Bir sonraki aşamada bu altyapı kullanılarak yavaş sorgular tespit edilecek ve uygun indeksleme (B-Tree vb.) yöntemleri ile optimizasyon sağlanacaktır.
## 3. Uzun Süren Sorguların Analizi ve Optimizasyonu
Sistemi yoran sorguları tespit etmek için `payment` tablosu üzerinde belirli bir tutarı (8.99) filtreleyen aşağıdaki sorgu çalıştırıldı:
`EXPLAIN ANALYZE SELECT customer_id, amount, payment_date FROM payment WHERE amount = 8.99;`

**Optimizasyon Öncesi Durum:**
Sorgu sonucunda veritabanının "Seq Scan" (Sıralı Tarama) yaptığı, aranan 438 kaydı bulmak için 14.158 satırı boşuna elediği ve toplam çalışma süresinin (Execution Time) **4.550 ms** olduğu tespit edildi.

**İndeksleme (B-Tree) İşlemi:**
Maliyetli olan bu okuma işlemini hızlandırmak için `amount` sütununa bir indeks tanımlandı:
`CREATE INDEX idx_payment_amount ON payment(amount);`

**Optimizasyon Sonrası Durum:**
İndeks oluşturulduktan sonra aynı sorgu tekrar çalıştırıldığında, veritabanının "Bitmap Index Scan" kullandığı ve çalışma süresinin **0.413 ms**'ye düştüğü gözlemlendi. Çalışma süresi yaklaşık 11 kat hızlanarak performans optimizasyonu başarıyla sağlandı.
