import json
import matplotlib.pyplot as plt
from collections import Counter
import os
import pandas as pd

DATA_FOLDER_PATH = "dane/v1/"
PLOTS_FOLDER_PATH = "plots/v1/"

def actions_in_session(file_name):
    file_path = os.path.abspath(DATA_FOLDER_PATH + file_name)
    actions = []

    # Otwórz plik i zlicz akcje
    with open(file_path, 'r') as file:
        for line in file:
            record = json.loads(line)
            if len(record) > 3 and record[3]:  # Sprawdź, czy pole akcji jest obecne
                actions.append(record[3])

    # Zlicz wystąpienia każdej akcji
    action_counts = Counter(actions)

    # Przygotuj dane do wykresu
    action_names = list(action_counts.keys())
    action_values = list(action_counts.values())

    # Oblicz procenty
    total_actions = sum(action_values)
    percentages = [(value / total_actions) * 100 for value in action_values]

    # Stwórz wykres kolumnowy
    plt.figure(figsize=(10, 6))
    bars = plt.bar(action_names, action_values)

    # Dodaj tytuły i opisy
    plt.title("Liczba wystąpień różnych akcji")
    plt.xlabel("Akcja")
    plt.ylabel("Liczba wystąpień")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Dodaj etykiety z procentami nad kolumnami
    for bar, percent in zip(bars, percentages):
        plt.text(
            bar.get_x() + bar.get_width() / 2,  # Środek kolumny
            bar.get_height(),  # Wysokość kolumny
            f'{percent:.1f}%',  # Format procentów
            ha='center', va='bottom'  # Wyśrodkowanie tekstu
        )

    # Pokaż wykres
    plt.savefig(PLOTS_FOLDER_PATH + "actions.png", format="png", dpi=300)

def storage_mode(file_path, path_to_save):
    storage_df = pd.read_json(os.path.abspath(DATA_FOLDER_PATH + file_path), lines=True)

    storage_counts = storage_df["storage_class"].value_counts()

    total = storage_counts.sum()
    percentages = (storage_counts / total) * 100

    print("\nLiczba wystąpień dla każdej klasy pamięci (z pominięciem wartości < 0.5%):")
    for label, value in zip(storage_counts.index.tolist(), storage_counts):
        print(f"- {label}: {value}")

    # Filtrowanie wartości bliskich zeru
    threshold = 0.5  # Procentowy próg
    significant_labels = percentages[percentages >= threshold].index.tolist()
    significant_values = percentages[percentages >= threshold].tolist()

    # Tworzenie wykresu kołowego
    plt.figure(figsize=(8, 6))
    plt.pie(
        significant_values,
        labels=significant_labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=plt.cm.tab20.colors[:len(significant_labels)],
    )
    plt.title("Procentowy udział każdej klasy pamięci (storage_class)")
    plt.savefig(PLOTS_FOLDER_PATH + path_to_save, format="png", dpi=300)

def analyze_skip_percentage(session_file, storage_file, storage_mode, path_to_save):
    """
    Analizuje procent utworów z różnymi klasami pamięci w przypadku akcji 'Skip'.
    """
    session_df = pd.read_json(os.path.abspath(DATA_FOLDER_PATH + session_file), lines=True)
    storage_df = pd.read_json(os.path.abspath(DATA_FOLDER_PATH + storage_file), lines=True)

    session_df.columns = ["timestamp", "user_id", "track_id", "action", "session_id"]

    # Filtruj dane dla akcji "Skip"
    skip_tracks = session_df[session_df["action"] == storage_mode]

    # Połącz dane na podstawie track_id
    merged_data = pd.merge(skip_tracks, storage_df, on="track_id", how="left")

    # Zlicz klasy pamięci dla utworów w akcji 'Skip'
    storage_counts = merged_data["storage_class"].value_counts()

    print(f"\nLiczba wystąpień dla każdej klasy pamięci w akcjach '{storage_mode}':")
    for storage_class, count in storage_counts.items():
        print(f"- {storage_class}: {count}")

    # Oblicz procentowy udział każdej klasy pamięci
    total_skips = storage_counts.sum()
    percentages = (storage_counts / total_skips) * 100

    # Przygotowanie danych do wykresu
    labels = percentages.index.tolist()  # Typy pamięci
    values = percentages.values          # Procenty

    # Tworzenie wykresu kołowego
    plt.figure(figsize=(8, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
    plt.title(f"Procent utworów z różnymi klasami pamięci w akcjach {storage_mode}")
    plt.savefig(PLOTS_FOLDER_PATH + path_to_save, format="png", dpi=300)

def main():
    actions_in_session('sessions.jsonl')
    analyze_skip_percentage('sessions.jsonl', 'track_storage.jsonl','Skip','SkipSession.png')
    analyze_skip_percentage('sessions.jsonl', 'track_storage.jsonl','Play','PlaySession.png')
    storage_mode('track_storage.jsonl', 'storage_mode.png')

main()