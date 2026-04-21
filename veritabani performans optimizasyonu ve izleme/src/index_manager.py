def create_btree_index(conn):
    try:
        cur = conn.cursor()
        cur.execute("CREATE INDEX idx_payment_amount ON payment(amount);")
        conn.commit()
        print("[BAŞARILI] idx_payment_amount B-Tree indeksi oluşturuldu.")
        cur.close()
    except Exception as e:
        print(f"İndeks oluşturulurken hata: {e}")