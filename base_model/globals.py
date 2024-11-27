from enum import Enum
import os

DATA_FOLDER_PATH = os.path.join("dane", "v1")

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