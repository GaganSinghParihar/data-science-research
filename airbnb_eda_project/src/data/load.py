# src/data/load.py
import pandas as pd


def load_with_dtypes(path: str, low_memory: bool = False):
    """Load CSV safely and return dataframe. Use low_memory=False to avoid mixed types."""
    df = pd.read_csv(path, low_memory=low_memory)
    return df




def infer_dtypes(df: pd.DataFrame):
    """
    Return a recommended dtype mapping (human-friendly categories).
    Does not coerce, only reports suggestions.
    """
    rec = {}

    for col in df.columns:
        ser = df[col]

        # direct dtype checks
        if pd.api.types.is_integer_dtype(ser):
            rec[col] = 'int'
            continue

        elif pd.api.types.is_float_dtype(ser):
            rec[col] = 'float'
            continue

        elif pd.api.types.is_bool_dtype(ser):
            rec[col] = 'bool'
            continue

        else:
            # check date-like
            try:
                parsed = pd.to_datetime(ser.dropna().iloc[:100], errors='coerce')
                if parsed.notna().sum() > 0:
                    rec[col] = 'datetime?'
                    continue
            except Exception:
                pass

            # numeric-like strings
            s = ser.dropna().astype(str)
            numeric_like = s.str.replace(',', '').str.match(r'^-?\d+(\.\d+)?$')

            if len(numeric_like) > 0 and numeric_like.sum() / max(1, len(numeric_like)) > 0.8:
                rec[col] = 'numeric_string'
                continue

            # low cardinality => category
            if ser.nunique(dropna=True) <= 100:
                rec[col] = 'category'
            else:
                rec[col] = 'string'

    return rec
