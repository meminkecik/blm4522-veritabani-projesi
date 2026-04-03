# [cite_start]Proje 3: Veritabanı Güvenliği ve Erişim Kontrolü [cite: 37]

## [cite_start]1. Kullanıcı Yetkilendirmesi ve Erişim Yönetimi [cite: 39]
Veritabanı güvenliğini sağlamak amacıyla farklı kullanıcı rolleri için erişim kısıtlamaları uygulanmıştır. Bu kapsamda 'stajyer' adında kısıtlı yetkilere sahip yeni bir kullanıcı rolü oluşturulmuştur.
Kullanılan komutlar:
`CREATE ROLE stajyer WITH LOGIN PASSWORD 'gizlisifre';`
`GRANT USAGE ON SCHEMA public TO stajyer;`
`GRANT SELECT ON actor TO stajyer;`

Bu rol ile sisteme giriş yapıldığında tablodan veri okuma (SELECT) işlemi başarıyla gerçekleşirken, veri silme (DELETE) girişimi veritabanı tarafından "permission denied" hatasıyla engellenmiş ve yetki kontrolünün başarıyla çalıştığı kanıtlanmıştır.

## [cite_start]2. Hassas Verilerin Şifrelenmesi (Data Encryption) 
Veritabanında tutulan kullanıcı şifreleri gibi hassas bilgilerin güvenliğini sağlamak için PostgreSQL'in `pgcrypto` eklentisi kullanılmıştır. Şifreler düz metin (plain text) yerine şifrelenmiş hash formatında saklanmıştır.
Kullanılan komut:
`INSERT INTO gizli_kullanicilar (kullanici_adi, sifre) VALUES ('yonetici', crypt('benim_gizli_sifrem_123', gen_salt('bf')));`

Veritabanı üzerinden yapılan sorgulamada şifrenin `$2a$06$...` formatında güvenli bir şekilde tutulduğu ve olası bir veri sızıntısında bile okunamayacak hale getirildiği doğrulanmıştır.
