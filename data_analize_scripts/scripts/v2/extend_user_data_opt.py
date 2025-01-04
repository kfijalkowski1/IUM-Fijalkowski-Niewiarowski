import pandas as pd
import os

# Wczytaj dane z pliku
sessions_path = os.path.join('data', "raw", "v2", "sessions_with_skip_like_and_duration_info_test_opt.jsonl")

# Wczytanie wszystkich danych
play_data = pd.read_json(sessions_path, lines=True)

# Sprawdź, czy dane nie są puste
if play_data.empty:
    raise ValueError("Plik wejściowy jest pusty. Upewnij się, że dane są poprawne.")

# Upewnij się, że 'user_id' jest w odpowiednim typie
play_data['user_id'] = play_data['user_id'].astype(int)

# Obliczenia dla użytkowników
user_stats = play_data.groupby('user_id').agg(
    avg_percent_played=('percent_played', lambda x: round(x.mean(), 2)),
    percent_full_tracks=('percent_played', lambda x: round((x==100).mean() * 100, 2))
).reset_index()

# Sprawdź, czy `user_stats` zawiera dane
if user_stats.empty:
    raise ValueError("Brak danych w `user_stats`. Upewnij się, że dane wejściowe są poprawne.")

# Dodanie informacji o średnim procencie odtworzenia użytkownika do wynikowych danych play_data
play_data = play_data.merge(user_stats[['user_id', 'avg_percent_played', 'percent_full_tracks']], on='user_id', how='left')

# Sprawdź, czy `avg_percent_played` została dodana
if 'avg_percent_played' not in play_data.columns:
    raise ValueError("Kolumna `avg_percent_played` nie została poprawnie dodana do `play_data`. Sprawdź dane i klucze.")

# Wypełnij brakujące wartości zerami (na wypadek brakujących dopasowań)
play_data['avg_percent_played'] = play_data['avg_percent_played'].fillna(0)
play_data['percent_full_tracks'] = play_data['percent_full_tracks'].fillna(0)

# Zapisz wyniki do pliku JSONL
output_sessions_path = os.path.join('data', "raw", "v2", "extended_data_opt.jsonl")
play_data[['timestamp', 'user_id', 'track_id', 'action', 'session_id', 'duration_time', 'percent_played', 'liked', 'skipped', 'avg_percent_played', 'percent_full_tracks']].to_json(output_sessions_path, orient='records', lines=True)

print(f'Wyniki zapisane do pliku: {output_sessions_path}')


