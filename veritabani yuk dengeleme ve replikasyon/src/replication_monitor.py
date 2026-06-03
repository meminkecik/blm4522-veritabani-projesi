import time
from src.db_connection import get_connection

def monitor_replication(rounds=3, interval=2):
    print("[MONİTOR] Replikasyon durumu izleniyor...")
    for i in range(rounds):
        conn = get_connection('primary')
        if not conn:
            print("[HATA] Primary'e bağlanılamadı.")
            return
        cur = conn.cursor()
        cur.execute("""
            SELECT client_addr, state, 
                   sent_lsn, write_lsn, flush_lsn, replay_lsn,
                   (sent_lsn - replay_lsn) AS lag_bytes
            FROM pg_stat_replication;
        """)
        rows = cur.fetchall()
        print(f"\n[MONİTOR] Tur {i+1}/{rounds}:")
        if not rows:
            print("  Henüz bağlanan replica yok.")
        for row in rows:
            print(f"  Replica IP : {row[0]}")
            print(f"  Durum      : {row[1]}")
            print(f"  Gecikme    : {row[6]} byte")
            print(f"  ---")
        cur.close()
        conn.close()
        if i < rounds - 1:
            time.sleep(interval)

def get_replica_count() -> int:
    conn = get_connection('primary')
    if not conn:
        return 0
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM pg_stat_replication;")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count