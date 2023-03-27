#%% Imports
import pandas as pd
from tqdm import tqdm

#--Scripts
import core.utils as utils

#%% Read in excel file of YouTube ID's of the FOMC press conferences
path2excel = 'TVOMP/Main/data/raw/fomc_all.xlsx'
excel = pd.read_excel(path2excel, 'QA_identifier')
yt_ids = excel['video_id'].drop_duplicates()
times  = excel['press_conf_time'].drop_duplicates()

#%% Loop through all of the YouTube videos
description = "Looping through the YouTube videos"
for yt_id, time in tqdm(zip(yt_ids, times), desc=description, total=len(yt_ids)):
    
    # Download the YouTube video
    fn, video_path, fps, date, length = utils.download_yt_vid(yt_id)
    # Print some useful outputs
    print(" ")
    print("   filename        : ", fn)
    print("   video_path      : ", video_path)
    print("   fps             : ", fps)
    print("   date            : ", date)
    print("   length (n_secs) : ", length)

    # Convert the mp4 of the YouTube video into frames
    save_freq = 2 # seconds
    utils.mp4_2_frames(video_path, save_freq, fps, time)

    # Print a new line 
    print(" ")