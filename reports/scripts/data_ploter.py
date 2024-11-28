import json
import matplotlib.pyplot as plt
from collections import Counter
import os
import pandas as pd
from ium_fij_niew.globals import DATA_FOLDER_PATH, PLOTS_FOLDER_PATH

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

def tracks_with_sessions(tracks_path, sessions_path, save = 'tracks_occurrence.png'):
    # Wczytanie danych
    tracks = pd.read_json(DATA_FOLDER_PATH + tracks_path, lines=True)
    sessions = pd.read_json(DATA_FOLDER_PATH + sessions_path, lines=True)

    # Zmiana nazw kolumn w sesjach dla przejrzystości
    sessions.columns = ["timestamp", "session_id", "track_id", "action", "user_id"]

    # Filtrowanie sesji, aby zachować tylko te, które mają prawidłowe identyfikatory utworów
    valid_sessions = sessions[sessions["track_id"].isin(tracks["id"])]

    # Liczba wystąpień każdego track_id w prawidłowych sesjach
    track_occurrences = valid_sessions["track_id"].value_counts()

    # Dodanie kolumny z liczbą wystąpień do tracks
    tracks["session_count"] = tracks["id"].map(track_occurrences).fillna(0).astype(int)

    # Podsumowanie danych
    no_sessions_count = (tracks["session_count"] == 0).sum()
    non_zero_sessions_count = (tracks["session_count"] > 0).sum()

    print(f"Liczba utworów bez sesji: {no_sessions_count}")
    print(f"Liczba utworów z co najmniej jedną sesją: {non_zero_sessions_count}")

    # Wykres: podział na utwory z i bez sesji
    counts = [non_zero_sessions_count, no_sessions_count]
    labels = ["Tracks with Sessions", "Tracks without Sessions"]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, counts, color=["green", "red"], alpha=0.75)
    plt.title("Tracks with and without Sessions")
    plt.ylabel("Number of Tracks")
    plt.xlabel("Track Presence in Sessions")
    plt.savefig(PLOTS_FOLDER_PATH + save, format="png", dpi=300)

def trac_popularity(tracks_path, sessions_path, save = 'tracks_popularity.png'):
    tracks = pd.read_json(DATA_FOLDER_PATH + tracks_path, lines=True)
    sessions = pd.read_json(DATA_FOLDER_PATH + sessions_path, lines=True)

    # Zmiana nazw kolumn w sesjach dla przejrzystości
    sessions.columns = ["timestamp", "session_id", "track_id", "action", "user_id"]

    # Filtrowanie sesji, aby zachować tylko te, które mają prawidłowe identyfikatory utworów
    valid_sessions = sessions[sessions["track_id"].isin(tracks["id"])]

    # Liczba wystąpień każdego track_id w prawidłowych sesjach
    track_occurrences = valid_sessions["track_id"].value_counts()

    # Dodanie kolumny z liczbą wystąpień do tracks
    tracks["session_count"] = tracks["id"].map(track_occurrences).fillna(0).astype(int)

    # Filtrowanie utworów z co najmniej jednym odtworzeniem
    filtered_tracks = tracks[tracks["session_count"] > 0].copy()  # Tworzenie kopii, aby uniknąć ostrzeżenia

    # Tworzenie dynamicznych binów
    max_session_count = filtered_tracks["session_count"].max()
    bins = list(range(1, min(max_session_count, 10) + 1)) + [max_session_count + 1]
    labels = [str(i) for i in range(1, len(bins))]  # Tworzenie etykiet: 1, 2, ..., 10+

    # Tworzenie przedziałów dla liczby odtworzeń
    filtered_tracks.loc[:, "play_count_range"] = pd.cut(filtered_tracks["session_count"], bins=bins, labels=labels, right=False)

    # Liczba utworów w każdej kategorii
    play_count_ranges = filtered_tracks["play_count_range"].value_counts().sort_index()

    # Wykres
    plt.figure(figsize=(10, 6))
    plt.bar(play_count_ranges.index.astype(str), play_count_ranges, alpha=0.75)
    plt.title("Track Play Count Distribution")
    plt.ylabel("Number of Tracks")
    plt.xlabel("Play Count")
    plt.xticks(rotation=0)
    plt.savefig(PLOTS_FOLDER_PATH + save, format="png", dpi=300)

def plot_genre_histogram_for_action(action, artists_path, sessions_path):
    artists = pd.read_json(DATA_FOLDER_PATH + artists_path, lines=True)
    sessions = pd.read_json(DATA_FOLDER_PATH + sessions_path, lines=True)

    artists.columns = ["artist_id", "artist_name", "genres"]
    sessions.columns = ["timestamp", "session_id", "track_id", "action", "user_id"]

    merged = sessions.merge(artists, left_on="track_id", right_on="artist_id", how="inner")

    filtered = merged[merged["action"] == action]

    filtered = filtered.explode("genres").dropna(subset=["genres"])

    genre_counts = filtered["genres"].value_counts()

    plt.figure(figsize=(12, 6))
    genre_counts.head(10).plot(kind="bar", alpha=0.75)
    plt.title(f"Top 10 Genres for Action: {action}")
    plt.xlabel("Genres")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(PLOTS_FOLDER_PATH + f'music_genres_{action}.png', format="png", dpi=300)

def plot_genre_histogram(artists_path, sessions_path):
    artists = pd.read_json(DATA_FOLDER_PATH + artists_path, lines=True)
    sessions = pd.read_json(DATA_FOLDER_PATH + sessions_path, lines=True)

    artists.columns = ["artist_id", "artist_name", "genres"]
    sessions.columns = ["timestamp", "session_id", "track_id", "action", "user_id"]

    merged = sessions.merge(artists, left_on="track_id", right_on="artist_id", how="inner")

    # Expand genres into individual rows
    merged = merged.explode("genres").dropna(subset=["genres"])

    # Count occurrences of genres
    genre_counts = merged["genres"].value_counts()

    # Plot the histogram
    plt.figure(figsize=(12, 6))
    genre_counts.plot(kind="bar", alpha=0.75)
    plt.title("Distribution of All Music Genres")
    plt.xlabel("Genres")
    plt.ylabel("Count")
    plt.xticks([])
    plt.tight_layout()
    plt.savefig(PLOTS_FOLDER_PATH + f'music_genres.png', format="png", dpi=300)
    plt.show()

def main():
    #actions_in_session('sessions.jsonl')
    #analyze_skip_percentage('sessions.jsonl', 'track_storage.jsonl','Skip','SkipSession.png')
    #analyze_skip_percentage('sessions.jsonl', 'track_storage.jsonl','Play','PlaySession.png')
    #storage_mode('track_storage.jsonl', 'storage_mode.png')
    #tracks_with_sessions('tracks.jsonl','sessions.jsonl')
    #trac_popularity('tracks.jsonl','sessions.jsonl')
    #plot_genre_histogram_for_action('Play', 'artists.jsonl', 'sessions.jsonl')
    #plot_genre_histogram_for_action('Like', 'artists.jsonl', 'sessions.jsonl')
    plot_genre_histogram('artists.jsonl', 'sessions.jsonl')

main()