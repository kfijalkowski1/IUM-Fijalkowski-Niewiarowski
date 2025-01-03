from ium_fij_niew.model_usage.model_classes import BaseModel, PredictResult, NormalModel
from fastapi import FastAPI
from pydantic import BaseModel as bs
import random
import json
import os

naive_model = BaseModel()
target_model = NormalModel()

predict = target_model.predict(101, "31PzY79H10HCgJs533Xq6B")

print(predict)

print(naive_model.predict(101, "31PzY79H10HCgJs533Xq6B"))
print(target_model.predict(101, "31PzY79H10HCgJs533Xq6B"))
print(target_model.predict(101, "31PzY79H10HCgJs533Xq6B"))
print(target_model.predict(101, "31PzY79H10HCgJs533Xq6B"))
print(target_model.predict(101, "31PzY79H10HCgJs533Xq6B"))

# Aplikacja FastAPI
app = FastAPI()

# Model danych wejściowych
class PredictionRequest(bs):
    user_id: int
    track_id: str

# Ścieżka do pliku logów
LOG_FILE_PATH = "model_usage_log.json"

# Inicjalizacja pliku logów, jeśli nie istnieje
if not os.path.exists(LOG_FILE_PATH):
    with open(LOG_FILE_PATH, "w") as log_file:
        json.dump([], log_file)

# Funkcja do zapisu logów
def append_to_log(entry):
    with open(LOG_FILE_PATH, "r") as log_file:
        logs = json.load(log_file)
    logs.append(entry)
    with open(LOG_FILE_PATH, "w") as log_file:
        json.dump(logs, log_file, indent=4)

# Endpoint dla modelu naiwnego
@app.post("/naive")
async def naive_predict(request: PredictionRequest):
    prediction = naive_model.predict(request.user_id, request.track_id)
    return prediction

# Endpoint dla modelu docelowego
@app.post("/recommend")
async def target_predict(request: PredictionRequest):
    prediction = target_model.predict(request.user_id, request.track_id)
    return prediction

@app.post("/abtest")
async def abtest(request: PredictionRequest):
    # Wybór modelu: 50/50 naiwnego i docelowego
    chosen_model = "naive" if random.random() < 0.5 else "target"

    if chosen_model == "naive":
        prediction = naive_model.predict(request.user_id, request.track_id)
    else:
        prediction = target_model.predict(request.user_id, request.track_id)

    # Konwersja PredictResult na tekstowy wynik
    if prediction == PredictResult.PLAY:
        prediction_output = "PLAY"
    elif prediction == PredictResult.SKIP:
        prediction_output = "SKIP"
    else:
        raise ValueError("Nieoczekiwany wynik predykcji")

    # Zapisanie informacji do pliku logów
    log_entry = {
        "model": chosen_model,
        "user_id": request.user_id,
        "track_id": request.track_id,
        "output": prediction_output
    }
    append_to_log(log_entry)

    # Zwrócenie wyniku predykcji
    return {
        "model": chosen_model,
        "user_id": request.user_id,
        "track_id": request.track_id,
        "prediction": prediction_output
    }

