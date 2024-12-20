import pandas as pd

# Wczytaj dane z pliku
data_path = './data_analize_scripts/dane/v1'
sessions_path = data_path + '/sessions.jsonl'

# Wczytywanie danych
columns = ['timestamp', 'user_id', 'track_id', 'action', 'session_id']
data = pd.read_json(sessions_path, lines=True)

# Nadanie kolumnom nazw
def rename_columns(df, new_columns):
    df.columns = new_columns

rename_columns(data, columns)

# Poprawa formatu strefy czasowej w kolumnie timestamp
data['timestamp'] = data['timestamp'].str.replace(" +02:00:00", " +02:00", regex=False)

# Konwersja kolumny timestamp na datetime
data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')

# Sprawdzenie i obsługa brakujących wartości w timestamp
if data['timestamp'].isnull().any():
    print("Warning: Some timestamps could not be parsed. Check the data for inconsistencies.")
    data = data.dropna(subset=['timestamp'])  # Usuń wiersze z brakującym timestampem

# Filtruj dane dla akcji "Play", "Skip" i "Like"
play_data = data[data['action'] == 'Play']
skip_data = data[data['action'] == 'Skip']
like_data = data[data['action'] == 'Like']

# Dołącz kolumny do identyfikacji tej samej sesji i utworu
play_data = play_data.copy()
play_data['skipped'] = False
play_data['liked'] = False
play_data['duration_time'] = None

# Iteruj po danych "Play" i sprawdzaj, czy istnieje odpowiednia akcja "Skip" i "Like"
for idx, play_row in play_data.iterrows():
    user_id = play_row['user_id']
    session_id = play_row['session_id']
    track_id = play_row['track_id']
    play_time = play_row['timestamp']

    # Sprawdź, czy play_time jest poprawny
    if pd.isnull(play_time):
        continue  # Pomiń wiersze z niepoprawnym timestampem

    # Znajdź odpowiednią akcję "Skip"
    corresponding_skip = skip_data[
        (skip_data['user_id'] == user_id) &
        (skip_data['session_id'] == session_id) &
        (skip_data['track_id'] == track_id) &
        (skip_data['timestamp'] > play_time)
    ]

    if not corresponding_skip.empty:
        # Weź najwcześniejszy timestamp "Skip"
        skip_time = corresponding_skip['timestamp'].min()

        # Upewnij się, że oba timestampy są w formacie datetime
        if pd.notnull(skip_time) and pd.notnull(play_time):
            duration_time = (skip_time - play_time).total_seconds()
        else:
            duration_time = None

        # Zaktualizuj kolumny "skipped" i "duration_time"
        play_data.at[idx, 'skipped'] = True
        play_data.at[idx, 'duration_time'] = duration_time

    # Znajdź odpowiednią akcję "Like"
    corresponding_like = like_data[
        (like_data['user_id'] == user_id) &
        (like_data['session_id'] == session_id) &
        (like_data['track_id'] == track_id)
    ]

    if not corresponding_like.empty:
        # Oznacz, że utwór został polubiony
        play_data.at[idx, 'liked'] = True

# Wynikowe dane
play_data['duration_time'] = play_data['duration_time'].astype(float, errors='ignore')  # Upewnij się, że kolumna ma odpowiedni typ

# Zapisz wyniki do pliku JSONL
output_path = data_path + '/sessions_with_skip_and_like_info.jsonl'
play_data.to_json(output_path, orient='records', lines=True)

print(f'Wyniki zapisane do pliku: {output_path}')
