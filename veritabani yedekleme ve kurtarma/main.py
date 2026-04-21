from src.db_connection import connect
from src.backup_manager import take_full_backup, restore_backup
from src.disaster_simulator import simulate_disaster, verify_table_exists
import time


def main():
    print("\n" + "=" * 50)
    print("--- PROJE 2: YEDEKLEME VE FELAKET KURTARMA OTOMASYONU ---")
    print("=" * 50)

    # 1. Aşama: Bağlantı ve Durum Kontrolü
    conn = connect()
    if not conn:
        return

    print("\n--- 1. AŞAMA: SİSTEM KONTROLÜ ---")
    verify_table_exists(conn, "payment")

    # 2. Aşama: Yedek Alma
    print("\n--- 2. AŞAMA: TAM YEDEKLEME (FULL BACKUP) ---")
    backup_file = take_full_backup()

    # 3. Aşama: Felaket Simülasyonu
    print("\n--- 3. AŞAMA: FELAKET SİMÜLASYONU (VERİ KAYBI) ---")
    simulate_disaster(conn)
    verify_table_exists(conn, "payment")  # Tablonun olmadığını kanıtlıyoruz

    # 4. Aşama: Kurtarma İşlemi
    print("\n--- 4. AŞAMA: FELAKETTEN KURTARMA (RESTORE) ---")
    conn.close()  # Geri yükleme yaparken bağlantıyı kapatmamız daha sağlıklıdır
    time.sleep(1)

    if backup_file:
        restore_backup(backup_file)

    # 5. Aşama: Kurtarma Sonrası Doğrulama
    print("\n--- 5. AŞAMA: KURTARMA SONRASI DOĞRULAMA ---")
    conn = connect()  # Tekrar bağlanıyoruz
    verify_table_exists(conn, "payment")  # Tablonun geri geldiğini kanıtlıyoruz
    conn.close()

    print("\n" + "=" * 50)
    print(">>> SÜREÇ BAŞARIYLA TAMAMLANDI <<<")
    print("=" * 50 + "\n")


if __name__ == '__main__':
    main()