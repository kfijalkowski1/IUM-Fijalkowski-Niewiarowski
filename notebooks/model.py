import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib

# Wczytanie danych
file_path = './data_analize_scripts/dane/v1/updated_sessions.jsonl'  # Podmień na właściwą ścieżkę
data = pd.read_json(file_path, lines=True)

# Filtracja danych
data = data.dropna(subset=['duration_ms', 'duration_time', 'percent_played', 'avg_percent_played', 'percent_completed'])

# Usunięcie rekordów z anomaliami
data = data[(data['duration_ms'] > 0) & 
            (data['duration_time'] >= 0) & 
            (data['percent_played'] >= 0) & (data['percent_played'] <= 100) &
            (data['avg_percent_played'] >= 0) & (data['avg_percent_played'] <= 100) &
            (data['percent_completed'] >= 0) & (data['percent_completed'] <= 100)]

# Tworzenie cech wejściowych
features = ['duration_ms', 'duration_time', 'avg_percent_played', 'percent_completed']
X = data[features]
y = data['percent_played']

# Skalowanie danych
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Podział na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Trening modelu
model = GradientBoostingRegressor(random_state=42, n_estimators=100, max_depth=5)
model.fit(X_train, y_train)

# Predykcja
y_pred = model.predict(X_test)

# Ewaluacja modelu
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
print(f"RMSE: {rmse:.2f}")
print(f"MAE: {mae:.2f}")

model_file_path = './models/v1/gradient_boosting_regressor.pkl'
joblib.dump(model, model_file_path)
print(f"Model zapisano do pliku: {model_file_path}")

# Przykładowe wyniki
print("Przykładowe przewidywania:")
results = pd.DataFrame({'Rzeczywisty procent': y_test, 'Przewidziany procent': y_pred}).head(10)
print(results)