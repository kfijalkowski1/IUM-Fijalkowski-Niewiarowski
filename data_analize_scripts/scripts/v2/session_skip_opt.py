import pandas as pd

# Wczytaj dane z pliku
data_path = './data_analize_scripts/dane/v2'
sessions_path = data_path + '/sessions.jsonl'
tracks_path = data_path + '/tracks.jsonl'

# Wczytanie wszystkich danych
data = pd.read_json(sessions_path, lines=True)

# Nadanie nazw kolumn
columns = ['timestamp', 'user_id', 'track_id', 'action', 'session_id']
data.columns = columns

# Poprawa formatu strefy czasowej w kolumnie timestamp
if data['timestamp'].dtype == 'object':
    data['timestamp'] = data['timestamp'].str.replace("+02", " +02:00", regex=False)

# Konwersja kolumny timestamp na datetime
data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')

# Sprawdzenie i obsługa brakujących wartości w timestamp
if data['timestamp'].isnull().any():
    print("Warning: Some timestamps could not be parsed. Check the data for inconsistencies.")
    data = data.dropna(subset=['timestamp'])

# Filtruj dane dla akcji "Play", "Skip" i "Like"
play_data = data[data['action'] == 'Play']
skip_data = data[data['action'] == 'Skip']
like_data = data[data['action'] == 'Like']

# Wczytaj dane o utworach (tracks)
tracks = pd.read_json(tracks_path, lines=True)
tracks.columns = [
    'track_id', 'artist_id', 'track_name', 'popularity', 'duration_ms', 'explicit', 
    'release_date', 'danceability', 'energy', 'key', 'mode', 'loudness', 
    'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 
    'tempo', 'time_signature'
]

# Połącz dane play_data z informacjami o utworach
play_data = play_data.merge(tracks[['track_id', 'duration_ms']], on='track_id', how='left')

# Dodaj kolumny do identyfikacji "skipped" i "liked"
play_data['skipped'] = False
play_data['liked'] = False
play_data['duration_time'] = None
play_data['percent_played'] = None

# Przyspieszenie przetwarzania za pomocą wektorowych operacji
# Dodanie kolumn pomocniczych
play_data = play_data.merge(skip_data, on=['user_id', 'session_id', 'track_id'], how='left', suffixes=('', '_skip'))
play_data['skip_time'] = play_data['timestamp_skip'] - play_data['timestamp']
play_data['duration_time'] = play_data['skip_time'].dt.total_seconds()

# Ustawienie czasu trwania jako pełnego czasu utworu, jeśli brak akcji "Skip"
play_data['duration_time'] = play_data['duration_time'].fillna(play_data['duration_ms'] / 1000)

# Obliczanie procentu odtworzenia
play_data['percent_played'] = (play_data['duration_time'] / (play_data['duration_ms'] / 1000)) * 100
play_data['percent_played'] = play_data['percent_played'].clip(upper=100)

# Dodanie informacji o "Liked"
play_data = play_data.merge(like_data, on=['user_id', 'session_id', 'track_id'], how='left', suffixes=('', '_like'))
play_data['liked'] = play_data['timestamp_like'].notnull()

# Wynikowe dane
play_data['duration_time'] = play_data['duration_time'].astype(float, errors='ignore')

# Zapisz wyniki do pliku JSONL
output_path = data_path + '/sessions_with_skip_like_and_duration_info_test_opt.jsonl'
play_data[['timestamp', 'user_id', 'track_id', 'action', 'session_id', 'duration_time', 'percent_played', 'liked', 'skipped']].to_json(output_path, orient='records', lines=True)

print(f'Wyniki zapisane do pliku: {output_path}')
