import pandas as pd
import matplotlib.pyplot as plt
import os


PLOTS_FOLDER_PATH = os.path.join("reports", "figures", "v1")

# Wczytanie danych
file_path = './data_analize_scripts/dane/v1/updated_sessions.jsonl'
data = pd.read_json(file_path, lines=True)

# Filtracja danych
data = data.dropna(subset=['percent_played'])

# Odrzucenie rekordów z anomaliami
data = data[(data['percent_played'] >= 0) & (data['percent_played'] <= 100)]

# Wyświetlenie histogramu dla kolumny 'percent_played'
plt.figure(figsize=(10, 6))
plt.hist(data['percent_played'], bins=20, edgecolor='k', alpha=0.7)
plt.title("Rozkład procentu przesłuchania utworów (percent_played)", fontsize=14)
plt.xlabel("Procent przesłuchania", fontsize=12)
plt.ylabel("Liczba utworów", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig(PLOTS_FOLDER_PATH + "/histogram.png", format="png", dpi=300)
plt.show()