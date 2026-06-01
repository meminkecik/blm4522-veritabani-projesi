import pandas as pd

def extract_from_postgres(engine) -> pd.DataFrame:
    query = """
        SELECT 
            p.payment_id,
            p.customer_id,
            p.staff_id,
            p.rental_id,
            p.amount,
            p.payment_date,
            c.first_name,
            c.last_name,
            c.email
        FROM payment p
        JOIN customer c ON p.customer_id = c.customer_id
    """
    df = pd.read_sql(query, engine)
    print(f"[EXTRACT] PostgreSQL'den {len(df)} kayıt çıkartıldı.")
    return df

def extract_from_csv(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, encoding='utf-8')
    print(f"[EXTRACT] CSV'den {len(df)} satır okundu.")
    print(f"[EXTRACT] Sütunlar: {list(df.columns)}")
    return df

def analyze_data_quality(df: pd.DataFrame, source_name: str):
    print(f"\n[ANALİZ] {source_name} ham veri kalitesi:")
    print(f"  Toplam kayıt       : {len(df)}")
    print(f"  Toplam sütun       : {len(df.columns)}")
    null_counts = df.isnull().sum()
    null_cols = null_counts[null_counts > 0]
    if len(null_cols) > 0:
        print(f"  Eksik değer (NULL) :")
        for col, count in null_cols.items():
            print(f"    → {col}: {count} adet")
    else:
        print(f"  Eksik değer        : Yok")
    duplicates = df.duplicated().sum()
    print(f"  Yinelenen kayıt    : {duplicates} adet")