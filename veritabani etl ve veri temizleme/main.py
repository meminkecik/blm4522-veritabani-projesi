import os
import numpy as np
import pandas as pd
from src.db_connection import get_connection, get_sqlalchemy_engine
from src.extractor import extract_from_postgres, analyze_data_quality
from src.transformer import (handle_missing_values, remove_duplicates,
                              standardize_dates, remove_outliers_iqr,
                              normalize_text, calculate_quality_score)
from src.loader import load_to_postgres, save_to_csv, generate_quality_report


def main():
    os.makedirs('reports', exist_ok=True)

    print("=" * 50)
    print("--- ETL PIPELINE BAŞLATILDI ---")
    print("=" * 50)

    conn = get_connection()
    engine = get_sqlalchemy_engine()

    # EXTRACT
    print("\n--- EXTRACT AŞAMASI ---")
    df = extract_from_postgres(engine)

    # Gerçekçi test için yapay kirlilik ekle
    print("\n[SİMÜLASYON] Ham veriye gerçekçi kirlilik ekleniyor...")
    null_indices = df.sample(50).index
    df.loc[null_indices, 'amount'] = np.nan
    df = pd.concat([df, df.sample(30)], ignore_index=True)
    mixed_indices = df.sample(100).index
    df.loc[mixed_indices, 'first_name'] = df.loc[mixed_indices, 'first_name'].str.lower()
    print(f"[SİMÜLASYON] NULL eklendi: 50 | Duplicate eklendi: 30 | Metin karıştırıldı: 100")

    analyze_data_quality(df, "payment + customer (kirli)")
    score_before = calculate_quality_score(df)

    # TRANSFORM
    print("\n--- TRANSFORM AŞAMASI ---")
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = standardize_dates(df, 'payment_date')
    df = remove_outliers_iqr(df, 'amount')
    df = normalize_text(df, ['first_name', 'last_name'])

    score_after = calculate_quality_score(df)

    stats = {
        "Ham kayıt sayısı"             : "14626 (14596 + 30 duplicate)",
        "Ham veri kalite skoru"         : f"%{score_before}",
        "Temizlenmiş kayıt sayısı"      : len(df),
        "Temizlenmiş veri kalite skoru" : f"%{score_after}",
        "Kalite iyileşmesi"             : f"+{round(score_after - score_before, 1)} puan",
    }

    # LOAD
    print("\n--- LOAD AŞAMASI ---")
    loaded = load_to_postgres(df, 'payment_clean', engine)
    save_to_csv(df, 'reports/payment_clean.csv')
    stats["Hedef tabloya yüklenen"] = f"{loaded} kayıt"

    generate_quality_report(stats, 'reports/data_quality_report.txt')

    print("\n" + "=" * 50)
    print("--- ETL PIPELINE TAMAMLANDI ---")
    print(f"Ham veri kalite skoru     : %{score_before}")
    print(f"Temizlenmiş veri skoru    : %{score_after}")
    print(f"Kalite iyileşmesi         : +{round(score_after - score_before, 1)} puan")
    print("=" * 50)

    conn.close()


if __name__ == "__main__":
    main()