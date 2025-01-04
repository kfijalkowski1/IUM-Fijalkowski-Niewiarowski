import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Wczytanie danych z pliku CSV
file_path = './data/processed/merged_data.csv'  # Zastąp ścieżką do swojego pliku
data = pd.read_csv(file_path)

# Lista wszystkich gatunków muzycznych
music_genres = [
    'adult standards', 'album rock', 'alternative metal', 'alternative rock', 'argentine rock', 
    'art rock', 'blues rock', 'brill building pop', 'c-pop', 'classic rock', 'country rock', 
    'dance pop', 'europop', 'folk', 'folk rock', 'funk', 'hard rock', 'hoerspiel', 
    'italian adult pop', 'j-pop', 'latin', 'latin alternative', 'latin pop', 'latin rock', 
    'lounge', 'mandopop', 'mellow gold', 'metal', 'modern rock', 'motown', 'mpb', 
    'new romantic', 'new wave', 'new wave pop', 'permanent wave', 'pop', 'pop rock', 
    'post-teen pop', 'psychedelic rock', 'quiet storm', 'ranchera', 'regional mexican', 
    'rock', 'rock en espanol', 'roots rock', 'singer-songwriter', 'soft rock', 'soul', 
    'tropical', 'vocal jazz'
]

# Usuwanie kolumn związanych z ID oraz preferencjami gatunków muzycznych
columns_to_remove = ['user_id', 'track_id', 'session_id', 'id'] + music_genres
data_cleaned = data.drop(columns=columns_to_remove, errors='ignore')

# Wybór kolumn do `ScaledTempo` włącznie
selected_columns = data_cleaned.loc[:, :'ScaledTempo']

# Usunięcie kolumn nienumerycznych z wybranego zakresu
selected_columns = selected_columns.select_dtypes(include=['float64', 'int64'])

# Obliczanie macierzy korelacji
correlation_matrix = selected_columns.corr()

# Wypisanie macierzy korelacji do konsoli
print("Macierz Korelacji:")
print(correlation_matrix)

# Wizualizacja macierzy korelacji bez liczb
plt.figure(figsize=(14, 12))
sns.heatmap(
    correlation_matrix,
    annot=False,  # Wyłącz liczby
    cmap='coolwarm',
    cbar=True,
    linewidths=1.5
)

# Dodanie tytułu i osi
plt.title('Macierz Korelacji', fontsize=18)
plt.xticks(rotation=90, ha='right', fontsize=12)
plt.yticks(fontsize=12)

# Zapisanie wykresu
plt.tight_layout()
plt.savefig('./reports/figures/v2/correlation_matrix_plot.png', dpi=300)  # Zapisz wykres w wysokiej jakości
plt.show()