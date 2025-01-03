import os.path
from abc import ABC, abstractmethod
from ium_fij_niew.base_model.base_model_test import check_if_user_likes_track
from ium_fij_niew.model_usage.data import get_parsed_data
from ium_fij_niew.utils import IncorrectData
from pickle import load
from enum import Enum

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