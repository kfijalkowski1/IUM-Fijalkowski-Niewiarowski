from pandas import DataFrame

import ium_fij_niew.utils as utils
import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler, MultiLabelBinarizer


def get_sessions_data():
    sessions_data = pd.DataFrame(pd.read_json(os.path.join(utils.DATA_FOLDER_PATH, "sessions.jsonl"), lines=True))
    sessions_data = sessions_data.drop(columns=["timestamp"])
    sessions_data = sessions_data[sessions_data["event_type"].isin(["Play", "Skip"])] # only play and skip events

    sessions_data = sessions_data.sort_values(by="event_type")  # Ensures 'Play' comes before 'Skip'
    # when there is skip and play for the same session_id and track_id, keep only skip, because it means
    # someone started listening and skipped
    sessions_data = sessions_data.drop_duplicates(subset=["session_id", "track_id"], keep="last")
    # Calculate User Skip Rate


    # Calculate Track Skip, user skip Rate and merge
    track_skip_rate = sessions_data.groupby("track_id")["event_type"].apply(
        lambda x: (x == "Skip").mean()
    ).reset_index(name="track_skip_rate")
    user_skip_rate = sessions_data.groupby("user_id")["event_type"].apply(
        lambda x: (x == "Skip").mean()
    ).reset_index(name="user_skip_rate")

    sessions_data = sessions_data.merge(user_skip_rate, on="user_id", how="left")
    sessions_data = sessions_data.merge(track_skip_rate, on="track_id", how="left")

    return sessions_data

def scale_data(merged_data):
    scaler = MinMaxScaler(feature_range=(0, 1))
    merged_data[["ScaledPopularity"]] = scaler.fit_transform(merged_data[["popularity"]])
    merged_data[["ScaledLoudness"]] = scaler.fit_transform(merged_data[["loudness"]])
    merged_data[["ScaledTempo"]] = scaler.fit_transform(merged_data[["tempo"]])


def one_hot_encoding_genres(merged_data):
    mlb = MultiLabelBinarizer()
    genres_binary = mlb.fit_transform(merged_data["favourite_genres"])
    genres_df = pd.DataFrame(genres_binary, columns=mlb.classes_)
    merged_data = pd.concat([merged_data, genres_df], axis=1)
    return merged_data


def parse_data():
    sessions_data = get_sessions_data()
    # load other data
    user_data =  pd.DataFrame(pd.read_json(os.path.join(utils.DATA_FOLDER_PATH, "users.jsonl"), lines=True))
    tracks_data = pd.DataFrame(pd.read_json(os.path.join(utils.DATA_FOLDER_PATH, "tracks.jsonl"), lines=True))

    # merge data
    merged_data_ses = sessions_data.merge(user_data[["user_id", "favourite_genres"]], on="user_id", how="inner")
    merged_data_ses = merged_data_ses[merged_data_ses["track_id"].notna()]
    merged_data = merged_data_ses.merge(tracks_data[
                                            ["id", "popularity", "danceability", "energy", "loudness", "speechiness",
                                            "acousticness", "instrumentalness", "liveness", "valence", "tempo"]],
                                        left_on="track_id", right_on="id", how="left")

    scale_data(merged_data)
    # one hot encoding of genres
    merged_data = one_hot_encoding_genres(merged_data)


    # encode event_type
    merged_data["event_type"] = merged_data["event_type"].map({"Play": 1, "Skip": 0})

    merged_data = merged_data.drop(columns=
                                   ["session_id", "id", "track_id", "user_id",
                                    "popularity", "loudness", "tempo", "favourite_genres"])
    validation_data = merged_data.sample(n=1000)
    merged_data = merged_data.drop(validation_data.index)


    y = merged_data[["event_type"]]
    y_valid = validation_data[["event_type"]]

    merged_data = merged_data.drop(columns=["event_type"])
    validation_data = validation_data.drop(columns=["event_type"])

    merged_data.to_csv(os.path.join(utils.PROCESSED_DATA_FOLDER_PATH, "merged_data.csv"), index=False)
    y.to_csv(os.path.join(utils.PROCESSED_DATA_FOLDER_PATH, "y.csv"), index=False)
    validation_data.to_csv(os.path.join(utils.PROCESSED_DATA_FOLDER_PATH, "validation_data.csv"), index=False)
    y_valid.to_csv(os.path.join(utils.PROCESSED_DATA_FOLDER_PATH, "validation_classes.csv"), index=False)

def check_if_files_exist(file_names: list[str]) -> bool:
    for file_name in file_names:
        if not os.path.exists(os.path.join(utils.PROCESSED_DATA_FOLDER_PATH, file_name)):
            return False
    return True



def get_data(force: bool=False) -> tuple[DataFrame, DataFrame, DataFrame, DataFrame]:
    """
    Creates data if force or if data doesn't exist
    and returns data for model training and validation

    """
    # load data from csv-s
    if force or not check_if_files_exist(["merged_data.csv", "y.csv", "validation_data.csv", "validation_classes.csv"]):
        parse_data()

    X = pd.read_csv(os.path.join(utils.PROCESSED_DATA_FOLDER_PATH, "merged_data.csv"))
    y = pd.read_csv(os.path.join(utils.PROCESSED_DATA_FOLDER_PATH, "y.csv"))['event_type'].to_numpy()
    validation_data = pd.read_csv(os.path.join(utils.PROCESSED_DATA_FOLDER_PATH, "validation_data.csv"))
    validation_classes = pd.read_csv(os.path.join(utils.PROCESSED_DATA_FOLDER_PATH, "validation_classes.csv"))['event_type'].to_numpy()
    return X, y, validation_data, validation_classes