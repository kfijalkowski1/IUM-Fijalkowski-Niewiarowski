import requests
import pandas as pd
import os

# Ścieżka do pliku z danymi testowymi
AB_TEST_DATA_PATH = "./data/processed/ab_test_data.csv"

# URL API
API_URL = "http://127.0.0.1:8000/abtest"

# Wczytaj dane do testu A/B
if not os.path.exists(AB_TEST_DATA_PATH):
    print(f"Plik {AB_TEST_DATA_PATH} nie istnieje.")
    exit(1)

ab_test_data = pd.read_csv(AB_TEST_DATA_PATH)

# Iteruj po rekordach i wysyłaj żądania do API
results = []
for _, row in ab_test_data.iterrows():
    payload = {
        "user_id": int(row["user_id"]),
        "track_id": row["track_id"]
    }

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Sprawdź, czy żądanie się powiodło
        result = response.json()
        results.append({
            "user_id": payload["user_id"],
            "track_id": payload["track_id"],
            "model": result["model"],
            "prediction": result["prediction"]
        })
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas wysyłania żądania: {e}")

# Zapisz wyniki testu A/B do pliku
output_path = "ab_test_results.csv"
pd.DataFrame(results).to_csv(output_path, index=False)
print(f"Wyniki testu A/B zapisano do {output_path}.")
