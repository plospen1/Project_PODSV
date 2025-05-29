import pandas as pd
import os

def clean_dataset3(file_path, save_path_csv):
    df = pd.read_excel(file_path, sheet_name="Tabelle1")

    raw_headers = df.iloc[5].tolist()
    clean_headers = []
    seen = {}
    for i, h in enumerate(raw_headers):
        if pd.isna(h) or str(h).strip() == "":
            h = f"Unnamed_{i}"
        else:
            h = str(h).strip()
        if h in seen:
            seen[h] += 1
            h = f"{h}_{seen[h]}"
        else:
            seen[h] = 1
        clean_headers.append(h)

    data = df.iloc[7:].copy()
    data.columns = clean_headers
    data = data.rename(columns={clean_headers[0]: "Year"})
    data = data[pd.to_numeric(data["Year"], errors="coerce").notnull()]
    data["Year"] = data["Year"].astype(int)
    data = data.iloc[:, 0:8]

    data.columns = [
        "Year", "Total", "Smallpox", "Scarlet_Fever", "Measles",
        "Typhoid_Paratyphoid", "Diphtheria", "Whooping_Cough"
    ]

    data.to_csv(save_path_csv, index=False)
    return data


def clean_dataset3_headers(file_path, save_path_csv):
    df = pd.read_excel(file_path)
    header_rows = df.iloc[3:6].fillna(method='ffill', axis=1)
    combined_headers = header_rows.apply(lambda x: ' | '.join(x.dropna().astype(str)), axis=0)

    data = df.iloc[9:].copy()
    data.columns = combined_headers
    data = data.reset_index(drop=True)

    data.to_csv(save_path_csv, index=False)
    return data


def load_all_data():
    base_path = "Data"

    # Cleaned datasets
    cleaned1_path = os.path.join(base_path, "data_set3_cleaned.csv")
    cleaned2_path = os.path.join(base_path, "dataset_3_cleaned_infectious_diseases.csv")

    # Falls die CSVs noch nicht existieren, erstelle sie
    if not os.path.exists(cleaned1_path):
        clean_dataset3_headers(os.path.join(base_path, "3_Todesursachen Schweiz ohne Alter 1876-2002.xlsx"), cleaned1_path)

    if not os.path.exists(cleaned2_path):
        clean_dataset3(os.path.join(base_path, "3_Todesursachen Schweiz ohne Alter 1876-2002.xlsx"), cleaned2_path)

    # Jetzt alle einlesen
    data = {
        "data_set1": pd.read_excel(os.path.join(base_path, "1_History_Pandemics.xlsx")),
        "data_set2_mortality": pd.read_excel(os.path.join(base_path, "2_All_cantons_1953-1958_Mortality.xlsx")),
        "data_set2_incidence_weekly": pd.read_excel(os.path.join(base_path, "2_Data_cantons_incidence_weekly_56_58_NEW.xlsx")),
        "data_set2_population": pd.read_excel(os.path.join(base_path, "2_Population_cantons.xlsx")),
        "data_set3": pd.read_excel(os.path.join(base_path, "3_Todesursachen Schweiz ohne Alter 1876-2002.xlsx")),
        "data_set3_cleaned": pd.read_csv(cleaned1_path),
        "data_covid": pd.read_csv(os.path.join(base_path, "full_data.csv")),
        "dataset3_infectdata": pd.read_csv(cleaned2_path),
    }

    return data


