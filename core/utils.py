#%% Imports
import os
import shutil
import glob
import numpy as np
import pandas as pd
import cv2
from tqdm import tqdm
from pytube import YouTube 

#--Scripts

#%% A function for downloading as YouTube video as an mp4
def download_yt_vid(yt_id, save_folder="data/mp4s"):

    # Define the download link
    link = "https://www.youtube.com/watch?v=" + yt_id

    # Create a yt object 
    try: 
        # object creation using YouTube
        # which was imported in the beginning 
        yt = YouTube(link) 
    except: 
        print("Connection Error") # to handle exception 

    # Get the mp4 files ordered from the highest resolution to the lowest resolution
    mp4files = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
    highest_res_mp4 = mp4files.first()

    # Define the title, the path, the fps, date, and the length
    title = yt.title
    fn   = title.replace(" ", "_").replace(",","") + '.mp4'
    fps  = highest_res_mp4.fps
    path = os.path.join(save_folder, fn)
    date = yt.publish_date
    length = yt.length

    # Download the YouTube video only if it has not already been downloaded
    if not os.path.exists(path):
        print("Downloading %s YouTube video..." % yt.title)
        highest_res_mp4.download(save_folder, fn)
    else:
        print("The %s YouTube video already exists..." % yt.title)

    # Return the fn, the path, the fps, date, and the length
    return fn, path, fps, date, length

#%% A function for creating time stamps of the video given the start time and the seconds
def create_timestamps(start_time, seconds):
    from datetime import datetime, timedelta
    timestamps = []
    for s in seconds:
        dt = start_time + timedelta(seconds=s)
        timestamps.append(dt.strftime("%Y-%m-%d %H:%M:%S"))

    return timestamps

# A function for converting an mp4 to image frames 
def mp4_2_frames(video_path, save_freq, fps, start_time):
    # Read in the mp4 file using cv2
    video      = cv2.VideoCapture(os.path.join(os.getcwd(), video_path))
    num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    # Use the .set function to set the frame number
    #---the first input is cv2.CAP_PROP_POS_FRAMES
    #---the second input is the 0-indexed frame number \in [0, num_frames-1]
    #---example: video.set(cv2.CAP_PROP_POS_FRAMES,num_frames-1) is the last frame of the video

    # Define the frame frames and the corresponding number of seconds into the video they are
    step = save_freq*fps
    frames  = np.arange(0, num_frames-1, step)
    seconds = frames / fps
    timestamps = create_timestamps(start_time, seconds)
    date = timestamps[0].split(" ")[0]

    # If the output save directory does not exist, create it 
    output_path = 'data/frames/%s' % date
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Loop through the frames and save them as pngs
    description = ("Writing frames from %s to %s" % (video_path, output_path))
    for frame_no, timestamp in tqdm(zip(frames, timestamps),desc=description, total=len(frames)):
        # Set the frame number
        video.set(cv2.CAP_PROP_POS_FRAMES,frame_no)
        # Read in the frame
        success, image = video.read()
        # Assert that the frame was read in properly
        assert success==True, "Frame %s (%s) was not read in properly in %s" % (frame_no, timestamp, video_path)
        # Define the output frame path
        frame_fn   = "%s.png" % timestamp.split(" ")[1]
        frame_path = os.path.join(output_path, frame_fn)
        # Write the output image
        cv2.imwrite(frame_path, image)

#%% Define a function for creating an excel sheet with the paths to the images that will be used to identify the chair
def get_identity_frames(conferences, save_path='data/identity_frames.xlsx'):
    dates = []
    identity_frames = []
    for conference in conferences:
        dates.append(os.path.basename(conference))
        frames = sorted(glob.glob(conference + '/*.png'))
        if os.path.basename(conference) == '2011-06-22':
            identity_frames.append(frames[30])
        elif os.path.basename(conference) == '2017-09-20':
            identity_frames.append(frames[21])
        else:
            identity_frames.append(frames[20])
    true_frames_excel = pd.DataFrame({'Date':dates, 'Identity Frame': identity_frames}).set_index('Date')
    true_frames_excel.to_excel(save_path)

#%% Define a function to save the identity frames
def save_identity_frames(excel_path='data/identity_frames.xlsx', save_path="data/identities"):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    identity_frames_excel = pd.read_excel(excel_path, index_col=0)
    for date, path in identity_frames_excel.iterrows():
        source = path['Identity Frame']
        target = os.path.join( save_path, date + "_" + os.path.basename(source) )
        shutil.copy(source, target)

#%% Define a simple function for getting the identity frame from the excel sheet from a date
def get_identity_frame_path(indentity_frames, conference):
    date = os.path.basename(conference)
    indentity_frame_path = indentity_frames.loc[date].values[0]
    return indentity_frame_path