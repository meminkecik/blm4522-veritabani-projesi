def create_roles(conn):
    cur = conn.cursor()
    try:
        # Önce bağımlı izinleri temizle
        cur.execute("REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM db_readonly_role;")
        cur.execute("REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM db_analyst_role;")
        cur.execute("REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM db_admin_role;")
        cur.execute("REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM db_readonly_role;")
        cur.execute("REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM db_analyst_role;")
        cur.execute("REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM db_admin_role;")
        # Kullanıcıları sil, sonra rolleri
        cur.execute("DROP USER IF EXISTS readonly_user;")
        cur.execute("DROP USER IF EXISTS analyst_user;")
        cur.execute("DROP USER IF EXISTS admin_user;")
        cur.execute("DROP ROLE IF EXISTS db_readonly_role;")
        cur.execute("DROP ROLE IF EXISTS db_analyst_role;")
        cur.execute("DROP ROLE IF EXISTS db_admin_role;")

        cur.execute("CREATE ROLE db_readonly_role;")
        cur.execute("CREATE ROLE db_analyst_role;")
        cur.execute("CREATE ROLE db_admin_role;")

        cur.execute("GRANT SELECT ON ALL TABLES IN SCHEMA public TO db_readonly_role;")
        cur.execute("GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA public TO db_analyst_role;")
        cur.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO db_admin_role;")

        cur.execute("CREATE USER readonly_user WITH PASSWORD 'Readonly@2025';")
        cur.execute("CREATE USER analyst_user WITH PASSWORD 'Analyst@2025';")
        cur.execute("CREATE USER admin_user WITH PASSWORD 'Admin@2025';")

        cur.execute("GRANT db_readonly_role TO readonly_user;")
        cur.execute("GRANT db_analyst_role TO analyst_user;")
        cur.execute("GRANT db_admin_role TO admin_user;")

        print("[BAŞARILI] RBAC rolleri ve kullanıcıları oluşturuldu.")
        print("  → db_readonly_role  : readonly_user  (sadece SELECT)")
        print("  → db_analyst_role   : analyst_user   (SELECT + INSERT)")
        print("  → db_admin_role     : admin_user      (tam yetki)")
    except Exception as e:
        print(f"[HATA] RBAC oluşturulurken hata: {e}")
    finally:
        cur.close()


def test_access_control(conn):
    cur = conn.cursor()
    print("\n--- RBAC ERİŞİM TESTİ ---")
    try:
        cur.execute("SELECT has_table_privilege('readonly_user', 'payment', 'SELECT');")
        print(f"[TEST] readonly_user → SELECT on payment : {cur.fetchone()[0]}")

        cur.execute("SELECT has_table_privilege('readonly_user', 'payment', 'DELETE');")
        print(f"[TEST] readonly_user → DELETE on payment : {cur.fetchone()[0]}")

        cur.execute("SELECT has_table_privilege('analyst_user', 'payment', 'INSERT');")
        print(f"[TEST] analyst_user  → INSERT on payment : {cur.fetchone()[0]}")

        cur.execute("SELECT has_table_privilege('admin_user', 'payment', 'DELETE');")
        print(f"[TEST] admin_user    → DELETE on payment : {cur.fetchone()[0]}")
    except Exception as e:
        print(f"[HATA] Erişim testi sırasında hata: {e}")
    finally:
        cur.close()