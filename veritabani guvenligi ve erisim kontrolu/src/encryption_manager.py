def enable_pgcrypto(conn):
    cur = conn.cursor()
    try:
        cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
        print("[BAŞARILI] pgcrypto eklentisi etkinleştirildi.")
    except Exception as e:
        print(f"[HATA] pgcrypto etkinleştirilemedi: {e}")
    finally:
        cur.close()


def encrypt_emails(conn, secret_key='gizli_anahtar_2025'):
    cur = conn.cursor()
    try:
        # Sütunu TEXT'e genişlet (base64 şifreli veri VARCHAR(50)'ye sığmıyor)
        cur.execute("""
            ALTER TABLE customer 
            ALTER COLUMN email TYPE TEXT;
        """)

        # Orijinal değerleri yedekle
        cur.execute("""
            ALTER TABLE customer 
            ADD COLUMN IF NOT EXISTS email_backup TEXT;
        """)
        cur.execute("""
            UPDATE customer 
            SET email_backup = email 
            WHERE email_backup IS NULL AND customer_id <= 10;
        """)

        # E-postaları şifrele
        cur.execute(f"""
            UPDATE customer
            SET email = encode(
                pgp_sym_encrypt(email, '{secret_key}'),
                'base64'
            )
            WHERE customer_id <= 10;
        """)
        print("[BAŞARILI] 10 müşteri e-postası AES ile şifrelendi.")
    except Exception as e:
        print(f"[HATA] Şifreleme hatası: {e}")
    finally:
        cur.close()


def decrypt_and_show(conn, secret_key='gizli_anahtar_2025'):
    cur = conn.cursor()
    try:
        cur.execute(f"""
            SELECT customer_id,
                   pgp_sym_decrypt(
                       decode(email, 'base64'),
                       '{secret_key}'
                   ) AS decrypted_email
            FROM customer
            WHERE customer_id <= 3;
        """)
        rows = cur.fetchall()
        print("[BAŞARILI] Şifreli veriler çözüldü:")
        for row in rows:
            print(f"  customer_id={row[0]} → {row[1]}")
    except Exception as e:
        print(f"[HATA] Şifre çözme hatası: {e}")
    finally:
        cur.close()


def restore_emails(conn):
    """Testi temizle — orijinal e-postaları geri yükle"""
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE customer
            SET email = email_backup
            WHERE customer_id <= 10 AND email_backup IS NOT NULL;
        """)
        cur.execute("ALTER TABLE customer DROP COLUMN IF EXISTS email_backup;")
        print("[TEMİZLENDİ] E-postalar orijinal haline geri yüklendi.")
    except Exception as e:
        print(f"[HATA] Geri yükleme hatası: {e}")
    finally:
        cur.close()


def mask_email(email: str) -> str:
    """Görüntüleme için e-posta maskele: john.doe@mail.com → jo****@mail.com"""
    if not email or '@' not in email:
        return '****'
    parts = email.split('@')
    masked = parts[0][:2] + '****' + '@' + parts[1]
    return masked