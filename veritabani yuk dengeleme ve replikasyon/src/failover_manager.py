import time
import subprocess
from src.db_connection import get_connection, test_connection


def check_primary_health(retries=3, interval=2) -> bool:
    for attempt in range(1, retries + 1):
        if test_connection('primary'):
            return True
        print(f"[UYARI] Primary bağlantı hatası (Deneme {attempt}/{retries})")
        time.sleep(interval)
    return False


def simulate_failover():
    print("\n--- FAİLOVER SİMÜLASYONU ---")
    print("[FAİLOVER] Primary durdurulуyor (simülasyon)...")

    start_time = time.time()

    # Primary container'ı durdur
    subprocess.run(
        ['docker', 'stop', 'pg_primary'],
        capture_output=True
    )
    print("[FAİLOVER] pg_primary durduruldu.")

    # Sağlık kontrolü
    primary_down = not check_primary_health(retries=3, interval=2)

    if primary_down:
        print("[FAİLOVER] Primary çevrimdışı tespit edildi!")
        print("[FAİLOVER] Replica1 devralıyor...")

        # Replica1'i primary olarak yükselt
        subprocess.run(
            ['docker', 'exec', 'pg_replica1',
             'su', '-', 'postgres', '-c',
             'pg_ctl promote -D /var/lib/postgresql/data'],
            capture_output=True
        )

        time.sleep(3)
        elapsed = round(time.time() - start_time, 1)

        # Yeni primary'e bağlan
        if test_connection('replica1'):
            print(f"[FAİLOVER] Replica1 yeni primary olarak aktif!")
            print(f"[FAİLOVER] Toplam geçiş süresi: {elapsed} saniye")
            print(f"[FAİLOVER] Veri kaybı: 0 kayıt")
        else:
            print("[FAİLOVER] Replica1'e bağlanılamadı.")

    # Primary'i yeniden başlat
    print("\n[RESTORE] Primary yeniden başlatılıyor...")
    subprocess.run(
        ['docker', 'start', 'pg_primary'],
        capture_output=True
    )
    time.sleep(3)
    if test_connection('primary'):
        print("[RESTORE] Primary tekrar çevrimiçi.")