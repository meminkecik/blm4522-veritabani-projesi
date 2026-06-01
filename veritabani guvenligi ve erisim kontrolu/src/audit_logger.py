import logging
import os

def setup_logger():
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        filename='logs/audit.log',
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    print("[BAŞARILI] Audit log altyapısı hazır → logs/audit.log")


def log_activity(username: str, action: str, table: str, status: str = "İZİN VERİLDİ"):
    message = f"KULLANICI: {username:<15} | İŞLEM: {action:<8} | TABLO: {table:<12} | DURUM: {status}"
    if status == "ENGELLENDİ":
        logging.warning(message)
    else:
        logging.info(message)
    print(f"[AUDIT LOG] {message}")