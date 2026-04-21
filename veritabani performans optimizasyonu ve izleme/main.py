from src.db_connection import connect
from src.performance_analyzer import run_explain_analyze
from src.index_manager import create_btree_index

def main():
    # 1. Veritabanına Bağlan
    conn = connect()
    if not conn:
        return

    # Testin doğru çalışması için önceki indeksleri temizle (Sıfırlama)
    cur = conn.cursor()
    cur.execute("DROP INDEX IF EXISTS idx_payment_amount;")
    conn.commit()
    cur.close()

    query = "SELECT customer_id, amount, payment_date FROM payment WHERE amount = 8.99;"

    print("\n" + "="*40)
    print("--- OPTİMİZASYON ÖNCESİ DURUM ---")
    time_before = run_explain_analyze(conn, query)

    print("\n" + "="*40)
    print("--- OPTİMİZASYON (İNDEKLEME) İŞLEMİ ---")
    create_btree_index(conn)

    print("\n" + "="*40)
    print("--- OPTİMİZASYON SONRASI DURUM ---")
    time_after = run_explain_analyze(conn, query)

    # Performans artışını hesapla
    if time_before and time_after:
        improvement = time_before / time_after
        print("\n" + "="*40)
        print(f">>> SONUÇ: Performans {improvement:.2f} kat artırıldı! <<<")
        print("="*40 + "\n")

    conn.close()

if __name__ == '__main__':
    main()