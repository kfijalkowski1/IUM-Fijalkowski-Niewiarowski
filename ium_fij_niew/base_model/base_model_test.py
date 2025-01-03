from typing import List
import os
import ium_fij_niew.utils as globals
import pandas as pd
import time

author_genre = {}
track_genre = {}

# load data only once

user_data = globals.create_dataframe_from_array("users.jsonl", globals.user_columns)
tracks_data = pd.DataFrame(pd.read_json(os.path.join(globals.DATA_FOLDER_PATH, "tracks.jsonl"), lines=True))
artists_data = globals.create_dataframe_from_array("artists.jsonl", globals.artist_columns)


def get_user_favorite_types(user_id: int) -> List[str]:
    """
    Get the favorite types of music for a given user.
    :param user_id: User ID
    :return: List of favorite types (genres)
    """
    user = user_data[user_data["user_id"] == user_id]
    if not user.empty:
        return user.iloc[0]["liked_genres"]
    return []


def get_track_author(track_id: str) -> str:
    """
    Get the artist_id of a track given its track_id.

    :param track_id: ID of the track
    :return: artist_id if found, None otherwise
    """
    filtered_data = tracks_data[tracks_data["id"] == track_id]
    if not filtered_data.empty:
        return filtered_data.iloc[0]["artist_id"]  # Access the first row's artist_id
    return ""


def cache_artist_genre(artist_id: str, genre: str):
    # save to dict for faster access
    global author_genre
    author_genre[artist_id] = genre

def cache_track_genre(track_id: str, genre: str):
    # save to dict for faster access
    global track_genre
    track_genre[track_id] = genre


def get_song_genre(track_id: str) -> List[str]:
    """
    Get the genre of a given song.
    :param track_id: Song ID
    :return: Genre of the song
    """
    # tracs.jsonl is a list of dics so we can use pandas
    artist_id = get_track_author(track_id)

    if artist_id is None:
        return []

    # check if we have it in cache
    if author_genre.get(artist_id) is not None:
        return author_genre.get(artist_id)

    filtered_data = artists_data[artists_data["artist_id"] == artist_id]
    if not filtered_data.empty:
        cache_artist_genre(artist_id, filtered_data.iloc[0]["genre"])
        cache_track_genre(track_id, filtered_data.iloc[0]["genre"])
        return filtered_data.iloc[0]["genre"]


def check_if_user_likes_track(user_id: int, track_id: str) -> bool:
    """
    Check if a user likes a given genre.
    :param user_id: User ID
    :param genre: Genre
    :return: True if the user likes the genre, False otherwise
    """
    user_fav_types = get_user_favorite_types(user_id)
    song_genre = get_song_genre(track_id)
    if not user_fav_types or not song_genre:
        raise globals.IncorrectData("No data for user or song")
    return any(genre in user_fav_types for genre in song_genre)



def test_if_user_should_skip():
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    incorrect_data = 0
    start_time = time.time()
    sessions_data = globals.create_dataframe_from_array("sessions.jsonl", globals.sessions_columns)
    for _, row in sessions_data.iterrows():
        try:
            play_recommended = check_if_user_likes_track(row["user_id"], row["track_id"])
        except globals.IncorrectData:
            incorrect_data += 1
            continue
        if row["action"] == "Play" and play_recommended:
            true_positive += 1
        if row["action"] == "Play" and not play_recommended:
            false_negative += 1
        if row["action"] == "Skip" and play_recommended:
            false_positive += 1
        if row["action"] == "Skip" and not play_recommended:
            true_negative += 1
    end_time = time.time()
    print("True positive: ", true_positive)
    print("True negative: ", true_negative)
    print("False positive: ", false_positive)
    print("False negative: ", false_negative)
    print("Incorrect data: ", incorrect_data)
    print("Time in seconds: ", end_time - start_time)
    print("Accuracy: ", (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative))
    print("Precision: ", true_positive / (true_positive + false_positive))
    print("Recall: ", true_positive / (true_positive + false_negative))