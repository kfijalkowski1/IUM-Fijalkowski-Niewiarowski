import os.path
from abc import ABC, abstractmethod
from ium_fij_niew.base_model.base_model_test import check_if_user_likes_track
from ium_fij_niew.model_usage.data import get_parsed_data
from ium_fij_niew.utils import IncorrectData
from pickle import load
from enum import Enum
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

class PredictResult(Enum):
    PLAY = 0
    SKIP = 1

class Model(ABC):
    @abstractmethod
    def predict(self, user_id: int, track_id: str) -> bool:
        """
        Predicts if a user will skip this track. return True if the user will skip the track, False otherwise
        """
        pass

class BaseModel(Model):
    def predict(self, user_id: int, track_id: str) -> PredictResult:
        """
        Predicts if a user will skip this track. return True if the user will skip the track, False otherwise
        """
        try:
            if check_if_user_likes_track(user_id, track_id):
                return PredictResult.PLAY
            else:
                return PredictResult.SKIP
        except IncorrectData as e:
            print(e)
            return PredictResult.SKIP

class NormalModel(Model):
    def __init__(self):
        with open(os.path.join("models", "linear_svc"), "rb") as f:
            self.model = load(f)

    def predict(self, user_id: int, track_id: str) -> PredictResult:
        """
        Predicts if a user will skip this track. return True if the user will skip the track, False otherwise
        """
        data_array = get_parsed_data(user_id, track_id)
        result = self.model.predict(data_array)
        if result == 1:
            return PredictResult.PLAY
        return PredictResult.SKIP
    
    def plot_feature_importance(self, file_path: str):
        """
        Generuje wykres istotności cech na podstawie modelu LinearSVC znajdującego się w Pipeline
        i zapisuje je w czterech osobnych plikach dla lepszej czytelności.

        Args:
            file_path (str): Ścieżka do pliku CSV zawierającego dane.
        """
        # Pobierz model LinearSVC z Pipeline
        if hasattr(self.model, 'named_steps'):
            linear_svc_model = self.model.named_steps.get('linearsvc')  # Użyj nazwy kroku w Pipeline
            if linear_svc_model is None:
                raise ValueError("Nie znaleziono modelu LinearSVC w Pipeline. Sprawdź nazwę kroku.")
        else:
            raise ValueError("Model nie jest obiektem Pipeline.")

        # Sprawdź, czy LinearSVC obsługuje atrybut `coef_`
        if not hasattr(linear_svc_model, 'coef_'):
            raise ValueError("Model LinearSVC nie obsługuje atrybutu 'coef_'.")

        # Wczytaj dane z pliku
        data = pd.read_csv(file_path)
        feature_names = list(data.columns)

        # Usuń kolumny nienumeryczne
        columns_to_remove = ['user_id', 'track_id', 'session_id', 'id', 'favourite_genres']
        feature_names = [col for col in feature_names if col not in columns_to_remove]

        # Pobierz współczynniki cech
        feature_importances = np.abs(linear_svc_model.coef_[0])  # Dla problemu binarnego

        # Dopasuj długość `feature_names` do `feature_importances`
        if len(feature_names) > len(feature_importances):
            feature_names = feature_names[:len(feature_importances)]
        elif len(feature_names) < len(feature_importances):
            feature_importances = feature_importances[:len(feature_names)]

        # Podział na cztery części
        num_parts = 4
        part_size = len(feature_names) // num_parts
        parts = [(feature_names[i:i + part_size], feature_importances[i:i + part_size])
                for i in range(0, len(feature_names), part_size)]

        # Generowanie wykresów
        for idx, (names, importances) in enumerate(parts):
            plt.figure(figsize=(10, 6))
            plt.barh(names, importances, color="skyblue")
            plt.xlabel("Ważność cechy", fontsize=14)
            plt.ylabel("Cechy", fontsize=14)
            plt.title(f"Wykres istotności cech {idx + 1}", fontsize=16)
            plt.tight_layout()

            # Zapis wykresu
            output_path = os.path.join("./reports/figures/v2/", f"feature_importance_part_{idx + 1}.png")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            plt.savefig(output_path, dpi=300)
            plt.close()

            print(f"Wykres zapisano do pliku: {output_path}")
