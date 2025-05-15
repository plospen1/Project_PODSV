# utils.py

import pandas as pd

def preprocess_data_set3(data_set3_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the raw dataset 3 (causes of death in Switzerland).
    
    - Combines multi-row headers
    - Cleans and resets the data
    """
    # Header-Zeilen kombinieren (Zeilen 4 bis 6)
    header_rows = data_set3_raw.iloc[3:6].fillna(method='ffill', axis=1)
    combined_headers = header_rows.apply(lambda x: ' | '.join(x.dropna().astype(str)), axis=0)

    # Effektive Daten ab Zeile 10 (Index 9)
    data = data_set3_raw.iloc[9:].copy()
    data.columns = combined_headers
    data = data.reset_index(drop=True)

    data.to_csv("../Data/data_set3_cleaned.csv")
    
    return data


