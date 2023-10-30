import os

import pandas as pd

from . import video_to_frame


def create_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print(f"Folder {path} doesn't exists... creating...")


def get_all_results(path, metric):
    results_files = os.listdir(path)

    for i, file in enumerate(results_files):
        if i == 0:
            df = pd.read_csv(path + "/" + file, sep="\t", na_values="     nan").dropna()
            df["u"] = df["u"].astype("float32")

        else:
            df_aux = pd.read_csv(
                path + "/" + file, sep="\t", na_values="     nan"
            ).dropna()
            df = pd.concat([df, df_aux])

    df.columns = ["x", "y", "u", "v", "mask"]

    return df.groupby(["x", "y"])[["u", "v"]].agg(metric).reset_index()


def get_movies_list(path, video_format: str = "h264"):
    return [i.split(".")[0] for i in os.listdir(path) if i.endswith(video_format)]


def transform_all_videos_to_frames(
    path: str = "data/videos/", video_format: str = "h264", qty_frames: int = 30
):
    videos = {}
    folders_list = [folder for folder in os.listdir(path) if folder != ".DS_Store"]

    for folder_name in folders_list:
        videos_folder = get_movies_list(path + folder_name, video_format)
        videos[folder_name] = videos_folder
        for video in videos_folder:
            video_to_frame.vf(
                path + folder_name + "/" + video + "." + video_format,
                qty_frames=qty_frames,
            )

    return videos
