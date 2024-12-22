import json
import pandas as pd

# Ścieżki do plików
data_path = './data_analize_scripts/dane/v1'
users_file = data_path + '/extended_users.jsonl'
sessions_file = data_path + '/sessions_with_skip_like_and_duration_info.jsonl'
track_storage_file = data_path + '/track_storage.jsonl'

# Wczytywanie danych do DataFrame
users_df = pd.read_json(users_file, lines=True)
sessions_df = pd.read_json(sessions_file, lines=True)
track_storage_df = pd.read_json(track_storage_file, lines=True)

sessions_df = sessions_df.merge(users_df[['user_id', 'avg_percent_played', 'percent_completed']], on='user_id', how='left')

# Mapowanie storage_class z track_storage do sesji
track_storage_mapping = track_storage_df.set_index('track_id')['storage_class'].to_dict()
sessions_df['storage_class'] = sessions_df['track_id'].map(track_storage_mapping)

# Zapisywanie wyniku do nowego pliku
output_file = data_path + '/updated_sessions.jsonl'
sessions_df.to_json(output_file, orient='records', lines=True)

print(f"Plik wynikowy zapisano do {output_file}")
