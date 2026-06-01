import psycopg2

def test_unsafe_query(conn, user_input="' OR '1'='1"):
    """SQL Injection'a açık güvensiz sorgu — SADECE TEST AMAÇLI"""
    cur = conn.cursor()
    try:
        # DİKKAT: Bu yöntem production'da ASLA kullanılmaz
        query = f"SELECT customer_id, first_name, last_name FROM customer WHERE last_name = '{user_input}'"
        cur.execute(query)
        results = cur.fetchall()
        print(f"[GÜVENLİK AÇIĞI] Güvensiz sorgu {len(results)} kayıt döndürdü! (Injection başarılı)")
    except Exception as e:
        print(f"[HATA] Güvensiz sorgu hatası: {e}")
    finally:
        cur.close()


def test_safe_query(conn, user_input="' OR '1'='1"):
    """Parametreli sorgu ile SQL Injection koruması"""
    cur = conn.cursor()
    try:
        query = "SELECT customer_id, first_name, last_name FROM customer WHERE last_name = %s"
        cur.execute(query, (user_input,))
        results = cur.fetchall()
        print(f"[KORUMALI] Güvenli sorgu {len(results)} kayıt döndürdü. (Injection engellendi)")
    except Exception as e:
        print(f"[HATA] Güvenli sorgu hatası: {e}")
    finally:
        cur.close()