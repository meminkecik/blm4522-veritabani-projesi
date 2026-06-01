import pandas as pd
from sqlalchemy import text

def load_to_postgres(df: pd.DataFrame, table_name: str, engine) -> int:
    try:
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            index=False,
            method='multi'
        )
        print(f"[LOAD] {len(df)} kayıt → '{table_name}' tablosuna yüklendi.")
        return len(df)
    except Exception as e:
        print(f"[HATA] Yükleme hatası: {e}")
        return 0

def save_to_csv(df: pd.DataFrame, filepath: str):
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"[LOAD] Temizlenmiş veri CSV'ye kaydedildi: {filepath}")

def generate_quality_report(stats: dict, filepath: str):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write("VERİ KALİTESİ RAPORU\n")
        f.write("=" * 50 + "\n\n")
        for key, value in stats.items():
            f.write(f"{key:<35}: {value}\n")
    print(f"[RAPOR] Veri kalitesi raporu oluşturuldu: {filepath}")