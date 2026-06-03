-- Replikasyon yetkisi ver
ALTER USER replicator REPLICATION;

-- Test verisi oluştur
CREATE TABLE IF NOT EXISTS test_replikasyon (
    id SERIAL PRIMARY KEY,
    mesaj TEXT,
    olusturma_zamani TIMESTAMP DEFAULT NOW()
);

INSERT INTO test_replikasyon (mesaj) VALUES
    ('Primary sunucudan ilk kayıt'),
    ('Replikasyon testi - kayıt 2'),
    ('Replikasyon testi - kayıt 3');

-- pg_hba.conf yerine host bazlı erişim için
SELECT pg_reload_conf();