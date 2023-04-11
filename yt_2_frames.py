#%% Imports
import pandas as pd
from tqdm import tqdm
import datetime

#--Scripts
import core.utils as utils

#%% Read in excel file of YouTube ID's 
# Define which YouTube links you want to look at
which_youtube_videos = 'trump'

# Frequency with which the frames will be saved
save_freq = 2 # seconds

if which_youtube_videos == 'trump':
    path2excel = 'data/yt_ids/trump_yt_ids.xlsx'
    excel = pd.read_excel(path2excel)
    yt_ids = excel['video_id'].drop_duplicates()
    save_folder = "data/mp4s/trump"
    frame_dir   = 'data/frames/trump'

elif which_youtube_videos == 'FOMC':
    path2excel = 'data/yt_ids/fomc_all.xlsx'
    excel = pd.read_excel(path2excel, 'QA_identifier')
    yt_ids = excel['video_id'].drop_duplicates()
    times  = excel['press_conf_time'].drop_duplicates()
    save_folder = "data/mp4s/FOMC"
    frame_dir   = 'data/frames/FOMC'

else:
    raise "%s is a not a valid input to which_youtube_ids" % which_youtube_videos

#%% Loop through all of the YouTube videos

description = "Looping through the YouTube videos"

if which_youtube_videos == 'FOMC':

    for yt_id, time in tqdm(zip(yt_ids, times), desc=description, total=len(yt_ids)):

        print('test', isinstance(time, datetime.datetime))
        
        # Download the YouTube video
        fn, video_path, fps, date, length = utils.download_yt_vid(yt_id, save_folder=save_folder)
        # Print some useful outputs
        print(" ")
        print("   filename   : ", fn)
        print("   video_path : ", video_path)
        print("   fps        : ", fps)
        print("   date       : ", date)
        print("   length     : ", length)

        # Convert the mp4 of the YouTube video into frames
        save_freq = 2 # seconds
        utils.mp4_2_frames(video_path, save_freq, fps, time, frame_dir=frame_dir)

        # Print a new line 
        print(" ")

else: 

    for yt_id in tqdm(yt_ids, desc=description, total=len(yt_ids)):
        
        # Get the upload timestamp of the YouTube video
        date, time, timestamp = utils.get_yt_upload_time(yt_id)
        # Download the YouTube video
        fn, video_path, fps, date, length = utils.download_yt_vid(yt_id, save_folder=save_folder)
        # Print some useful outputs
        print(" ")
        print("   filename   : ", fn)
        print("   video_path : ", video_path)
        print("   fps        : ", fps)
        print("   date       : ", date)
        print("   time       : ", time)
        print("   timestamp  : ", timestamp)
        print("   length     : ", length)

        # Convert the mp4 of the YouTube video into frames
        utils.mp4_2_frames(video_path, save_freq, fps, timestamp, frame_dir=frame_dir)

        # Print a new line 
        print(" ")