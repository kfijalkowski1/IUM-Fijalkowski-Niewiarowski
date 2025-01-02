import pandas as pd

def rename_columns(df, new_columns):
    df.columns = new_columns

# Wczytaj dane z plików
data_path = './data_analize_scripts/dane/v1'
users_path = data_path + '/users.jsonl'
sessions_with_path = data_path + '/sessions_with_skip_like_and_duration_info.jsonl'

users = pd.read_json(users_path, lines=True)
rename_columns(users, ['user_id', 'name', 'city', 'street', 'top', 'unknown'])
sessions_with = pd.read_json(sessions_with_path, lines=True)

# Obliczenia dla użytkowników
user_stats = sessions_with.groupby('user_id').agg(
    total_tracks=('track_id', 'count'),
    completed_tracks=('percent_played', lambda x: (x == 100).sum()),
    avg_percent_played=('percent_played', lambda x: round(x.mean(), 2))
).reset_index()


# Oblicz procent utworów przesłuchanych do końca
user_stats['percent_completed'] = round((user_stats['completed_tracks'] / user_stats['total_tracks']) * 100, 2)

# Połącz dane użytkowników z obliczonymi statystykami
users = users.merge(user_stats, on='user_id', how='left')

# Wypełnij brakujące wartości zerami, jeśli użytkownik nie ma danych
users['percent_completed'] = users['percent_completed'].fillna(0)
users['avg_percent_played'] = users['avg_percent_played'].fillna(0)

# Zapisz rozszerzone dane użytkowników do nowego pliku JSONL
output_path = data_path + '/extended_users.jsonl'
users.to_json(output_path, orient='records', lines=True)

print(f'Rozszerzone dane użytkowników zapisano do pliku: {output_path}')
