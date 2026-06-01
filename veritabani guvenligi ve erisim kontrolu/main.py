from src.db_connection import get_connection
from src.rbac_manager import create_roles, test_access_control
from src.encryption_manager import enable_pgcrypto, encrypt_emails, decrypt_and_show, restore_emails, mask_email
from src.injection_tester import test_unsafe_query, test_safe_query
from src.audit_logger import setup_logger, log_activity

def main():
    print("=" * 50)
    print("--- VERİTABANI GÜVENLİK TESTLERİ ---")
    print("=" * 50)

    conn = get_connection()

    # 1. Audit log altyapısını kur
    setup_logger()

    # 2. RBAC
    print("\n--- ROL TABANLI ERİŞİM KONTROLÜ (RBAC) ---")
    create_roles(conn)
    test_access_control(conn)
    log_activity("readonly_user", "SELECT", "payment")
    log_activity("readonly_user", "DELETE", "payment", "ENGELLENDİ")
    log_activity("admin_user",    "DELETE", "payment")

    # 3. Şifreleme
    print("\n--- ŞİFRELEME TESTİ ---")
    enable_pgcrypto(conn)
    encrypt_emails(conn)
    decrypt_and_show(conn)

    # E-posta maskeleme örneği
    test_email = "john.doe@sakilacustomer.org"
    print(f"[MASKELEME] {test_email} → {mask_email(test_email)}")

    # Testi temizle
    restore_emails(conn)

    # 4. SQL Injection
    print("\n--- SQL INJECTION TESTİ ---")
    test_unsafe_query(conn)
    test_safe_query(conn)
    log_activity("hacker",       "SELECT", "customer", "ENGELLENDİ")
    log_activity("analyst_user", "SELECT", "customer")

    print("\n" + "=" * 50)
    print("Tüm testler tamamlandı. Audit log: logs/audit.log")
    print("=" * 50)

    conn.close()

if __name__ == "__main__":
    main()