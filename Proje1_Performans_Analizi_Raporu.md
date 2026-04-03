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
