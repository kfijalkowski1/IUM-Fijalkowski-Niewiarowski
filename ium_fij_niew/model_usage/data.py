import os.path

import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np

from ium_fij_niew.normal_model.data_parser import get_sessions_data, scale_data, one_hot_encoding_genres
from ium_fij_niew.utils import DATA_FOLDER_PATH

"""
This package is for preparing data form model to predict.
Model expects data in the following format:

user_skip_rate,track_skip_rate,danceability,energy,speechiness,acousticness,instrumentalness,liveness,valence,
ScaledPopularity,ScaledLoudness,ScaledTempo,adult standards,album rock,alternative metal,alternative rock,argentine rock,
art rock,blues rock,brill building pop,c-pop,classic rock,country rock,dance pop,europop,folk,folk rock,funk,hard rock,hoerspiel,
italian adult pop,j-pop,latin,latin alternative,latin pop,latin rock,lounge,mandopop,mellow gold,metal,modern rock,motown,mpb,
new romantic,new wave,new wave pop,permanent wave,pop,pop rock,post-teen pop,psychedelic rock,quiet storm,ranchera,regional mexican,
rock,rock en espanol,roots rock,singer-songwriter,soft rock,soul,tropical,vocal jazz
"""

HISTORY_SESSIONS = get_sessions_data()
TRACKS_DATA = pd.DataFrame(pd.read_json(os.path.join(DATA_FOLDER_PATH, "tracks.jsonl"), lines=True))
scale_data(TRACKS_DATA)
USER_DATA = pd.DataFrame(pd.read_json(os.path.join(DATA_FOLDER_PATH, "users.jsonl"), lines=True))
USER_DATA = one_hot_encoding_genres(USER_DATA)
USER_DATA.drop(columns=["name", "city", "street", "favourite_genres", "premium_user"], inplace=True)

def get_parsed_data(user_id, track_id):
    """
    Get data in the format expected by the model.

    :param user_id: ID of the user
    :param track_id: ID of the track
    :return: Data in the format expected by the model
    """
    user_data = USER_DATA[USER_DATA["user_id"] == user_id]
    track_data = TRACKS_DATA[TRACKS_DATA["id"] == track_id]

    if user_data.empty or track_data.empty:
        return None


    user_skip_rate = HISTORY_SESSIONS[HISTORY_SESSIONS["user_id"] == user_id]["user_skip_rate"].mean()
    track_skip_rate = HISTORY_SESSIONS[HISTORY_SESSIONS["track_id"] == track_id]["track_skip_rate"].mean()

    user_data = user_data.drop(columns=["user_id"])

    track_features = track_data[[
        "danceability", "energy", "speechiness", "acousticness", "instrumentalness",
        "liveness", "valence", "ScaledPopularity", "ScaledLoudness", "ScaledTempo"
    ]].iloc[0].tolist()

    # Prepare user data
    user_features = user_data.iloc[0].tolist()


    final_features = [user_skip_rate, track_skip_rate] + track_features + user_features

    result = np.array(final_features).reshape(1, -1)

    return result


