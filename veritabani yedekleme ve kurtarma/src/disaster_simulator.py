def simulate_disaster(conn):
    try:
        cur = conn.cursor()
        print("[FELAKET] 'payment' tablosu ve bağlı view'lar kasti olarak siliniyor...")
        cur.execute("DROP TABLE payment CASCADE;")
        conn.commit()
        print("[BAŞARILI FELAKET] Veriler tamamen yok edildi!")
        cur.close()
    except Exception as e:
        print(f"[HATA] Felaket simülasyonu başarısız: {e}")

def verify_table_exists(conn, table_name):
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cur.fetchone()[0]
        print(f"[KONTROL] '{table_name}' tablosu SAĞLAM. İçinde {count} adet kayıt var.")
        cur.close()
        return True
    except Exception:
        print(f"[KONTROL HATA] '{table_name}' tablosu BULUNAMADI! (Veri Kaybı)")
        conn.rollback() # Hatayı yoksay ve devam et
        return False