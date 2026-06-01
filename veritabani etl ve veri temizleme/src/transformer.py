import pandas as pd
import numpy as np

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    null_before = df.isnull().sum().sum()

    for col in df.select_dtypes(include=[np.number]).columns:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"  [NULL] {col}: boş değerler medyan ({median_val:.2f}) ile dolduruldu.")

    for col in df.select_dtypes(include=['object']).columns:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna('BILINMIYOR')
            print(f"  [NULL] {col}: boş değerler 'BILINMIYOR' ile dolduruldu.")

    null_after = df.isnull().sum().sum()
    print(f"[TRANSFORM] Eksik değer: {null_before} → {null_after}")
    return df

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"[TRANSFORM] Yinelenen kayıt kaldırıldı: {before - after} adet ({before} → {after})")
    return df

def standardize_dates(df: pd.DataFrame, col: str) -> pd.DataFrame:
    if col not in df.columns:
        return df
    before_nulls = df[col].isnull().sum()
    df[col] = pd.to_datetime(df[col], errors='coerce')
    after_nulls = df[col].isnull().sum()
    df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
    fixed = after_nulls - before_nulls
    print(f"[TRANSFORM] {col} ISO 8601 formatına dönüştürüldü. (Hatalı format: {fixed} adet)")
    return df

def remove_outliers_iqr(df: pd.DataFrame, col: str) -> pd.DataFrame:
    if col not in df.columns:
        return df
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    before = len(df)
    df = df[(df[col] >= lower) & (df[col] <= upper)]
    removed = before - len(df)
    print(f"[TRANSFORM] Aykırı değer ({col}): {removed} kayıt kaldırıldı. (Alt:{lower:.2f}, Üst:{upper:.2f})")
    return df

def normalize_text(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    for col in cols:
        if col in df.columns:
            df[col] = df[col].str.strip().str.upper()
    print(f"[TRANSFORM] Metin normalizasyonu tamamlandı: {cols}")
    return df

def calculate_quality_score(df: pd.DataFrame) -> float:
    total_cells = df.shape[0] * df.shape[1]
    null_cells = df.isnull().sum().sum()
    duplicate_cells = df.duplicated().sum() * df.shape[1]
    bad_cells = null_cells + duplicate_cells
    score = ((total_cells - bad_cells) / total_cells) * 100
    return round(score, 1)