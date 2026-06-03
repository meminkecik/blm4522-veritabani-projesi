import time
from src.db_connection import test_connection
from src.replication_monitor import monitor_replication, get_replica_count
from src.load_balancer import run_load_balance_test
from src.failover_manager import check_primary_health, simulate_failover

def main():
    print("=" * 50)
    print("--- YÜK DENGELEME VE REPLİKASYON TESTİ ---")
    print("=" * 50)

    # Bağlantı kontrolleri
    print("\n--- BAĞLANTI KONTROLÜ ---")
    for node in ['primary', 'replica1', 'replica2']:
        status = "✓ AKTİF" if test_connection(node) else "✗ KAPALI"
        print(f"  {node:<12}: {status}")

    replica_count = get_replica_count()
    print(f"\n[BİLGİ] Primary'e bağlı replica sayısı: {replica_count}")

    if replica_count == 0:
        print("[UYARI] Henüz replica bağlanmamış. Docker cluster başlatıldı mı?")
        print("  → cd docker && docker compose up -d")
        return

    # Replikasyon izleme
    print("\n--- REPLİKASYON İZLEME ---")
    monitor_replication(rounds=2, interval=2)

    # Yük dengeleme testi
    run_load_balance_test()

    # Failover testi
    print("\n--- FAİLOVER TESTİ ---")
    cevap = input("Failover simülasyonu başlatılsın mı? (e/h): ")
    if cevap.lower() == 'e':
        simulate_failover()

    print("\n" + "=" * 50)
    print("Tüm testler tamamlandı.")
    print("=" * 50)

if __name__ == "__main__":
    main()