from itertools import cycle
from src.db_connection import get_connection

REPLICA_SECTIONS = cycle(['replica1', 'replica2'])

def route_query(query: str, params=None):
    query_upper = query.strip().upper()
    if query_upper.startswith(('INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER')):
        target = 'primary'
    else:
        target = next(REPLICA_SECTIONS)

    conn = get_connection(target)
    if not conn:
        print(f"[LOAD BALANCER] {target} bağlanamadı, primary'e yönlendiriliyor.")
        conn = get_connection('primary')

    cur = conn.cursor()
    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)

    if query_upper.startswith('SELECT'):
        result = cur.fetchall()
        print(f"[LOAD BALANCER] SELECT → {target} | {len(result)} kayıt döndü.")
        cur.close()
        conn.close()
        return result
    else:
        print(f"[LOAD BALANCER] WRITE → {target} | İşlem tamamlandı.")
        cur.close()
        conn.close()
        return None

def run_load_balance_test():
    print("\n--- YÜK DENGELEME TESTİ (6 SELECT + 1 INSERT) ---")
    for i in range(1, 7):
        result = route_query("SELECT COUNT(*) FROM test_replikasyon;")
        print(f"  Sorgu {i}: {result[0][0]} kayıt")

    route_query(
        "INSERT INTO test_replikasyon (mesaj) VALUES (%s);",
        ("Load balancer testi - yazma işlemi",)
    )