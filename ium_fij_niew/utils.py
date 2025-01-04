from enum import Enum
import os
import pandas as pd
from typing import List

DATA_FOLDER_PATH = os.path.join("data", "raw", "v2")
PROCESSED_DATA_FOLDER_PATH = os.path.join("data", "processed")
PLOTS_FOLDER_PATH = os.path.join("reports", "figures")

# users table indexes
class UserTableIndex(Enum):
    user_id = 0
    name = 1
    adress1 = 2
    address2 = 3
    liked_genres = 4
    unknown = 5

class ArtistTableIndex(Enum):
    artist_id = 0
    name = 1
    genre = 2

class SessionsTableIndex(Enum):
    session_date = 0
    user_id = 1
    track_id = 2
    action = 3
    unknown = 4



class IncorrectData(Exception):
    pass


# column typpes
user_columns = ["user_id", "name", "address1", "address2", "liked_genres", "unknown"]
artist_columns = ["artist_id", "artist_name", "genre"]
sessions_columns = ["session_date", "user_id", "track_id", "action", "unknown"]


def create_dataframe_from_array(path: str, columns: List[str]) -> pd.DataFrame:
    global DATA_FOLDER_PATH
    data = pd.DataFrame(pd.read_json(os.path.join(DATA_FOLDER_PATH, path), lines=True))
    data.transpose()
    data.columns = columns
    return data

