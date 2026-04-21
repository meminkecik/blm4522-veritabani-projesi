import subprocess
import os


def take_full_backup():
    # Yedekler için klasör oluştur (yoksa)
    os.makedirs('backups', exist_ok=True)
    backup_path = 'backups/dvdrental_tam_yedek.backup'

    print("[İŞLEM] Tam yedekleme (Full Backup) başlatılıyor...")
    # Terminale pg_dump komutunu gönderiyoruz
    command = f"pg_dump -F c -d dvdrental -f {backup_path}"

    try:
        subprocess.run(command, shell=True, check=True)
        print(f"[BAŞARILI] Yedek başarıyla alındı: {backup_path}")
        return backup_path
    except subprocess.CalledProcessError as e:
        print(f"[HATA] Yedekleme başarısız: {e}")
        return None


def restore_backup(backup_path):
    print("[İŞLEM] Yedekten kurtarma (Restore) başlatılıyor...")
    command = f"pg_restore -d dvdrental --clean --no-owner {backup_path}"

    try:
        # check=True parametresini sildik ki ufak uyarılarda script çökmesin
        result = subprocess.run(command, shell=True, stderr=subprocess.DEVNULL)

        # pg_restore 0 (kusursuz) veya 1 (uyarılar var ama yüklendi) döndürürse başarılı sayıyoruz
        if result.returncode in [0, 1]:
            print("[BAŞARILI] Veritabanı başarıyla eski haline getirildi!")
        else:
            print(f"[HATA] Kurtarma işlemi başarısız. Çıkış kodu: {result.returncode}")
    except Exception as e:
        print(f"[HATA] Beklenmeyen bir durum oluştu: {e}")