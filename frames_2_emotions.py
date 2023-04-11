#%% Imports
import glob
import os
import pandas as pd

#--Scripts
import core.utils as utils
import core.face as face

#%% Input toggle(s)
# You need to run yt_2_frames.py with the same which_youtube_videos before running this script
which_youtube_videos = 'trump'

verify     = False # A toggle that if True will verify that the frame contains the speaker
all_videos = True  # A toggle that if True will apply DeepFace to all of the videos

if which_youtube_videos == 'trump':
    frames_dir = 'data/frames/trump/'
    save_path  = 'data/emotions/trump/'
    identity_frames_excel_path = 'data/identities/trump.xlsx'
    identity_frames_frame_path = 'data/identities/trump_frames/'

elif which_youtube_videos == 'FOMC':
    frames_dir = 'data/frames/FOMC/'
    save_path  = 'data/emotions/FOMC/'
    identity_frames_excel_path = 'data/identities/FOMC.xlsx'
    identity_frames_frame_path = 'data/identities/FOMC_frames/'

else:
    raise "%s is a not a valid input to which_youtube_ids" % which_youtube_videos

#%% Define the frames from the videos that will be used to verify the identity of the speaker
videos = sorted(glob.glob(os.path.join(frames_dir, '*')))
# Define the frames in the video that will be used to identify the speaker and save their paths to an excel file
utils.get_identity_frames(videos, save_path=identity_frames_excel_path)
# Save the identity frames to a new folder to verify they contain the speaker
utils.save_identity_frames(excel_path=identity_frames_excel_path, save_path=identity_frames_frame_path)

#%% Loop through the videos and predict the emotions for all of the frames in the videos
if all_videos:
    indentity_frames = pd.read_excel(identity_frames_excel_path, index_col=0)
    if verify:
        face.predict_all_emotions(videos, indentity_frames, save_path=save_path)
    else:
        face.predict_all_emotions(videos, save_path=save_path)

#%% Debug one particular conference if the verification is struggling
# indentity_frames = pd.read_excel(identity_frames_excel_path, index_col=0)
# conference_of_interest = videos[0]
# num_frames = None
# print(conference_of_interest)
# if verify:
#     indentity_frame_path = utils.get_identity_frame_path(conference_of_interest, indentity_frames)
#     emotions_df = face.predict_emotions(conference_of_interest, indentity_frame_path, num_frames=num_frames)
# else:
#     emotions_df = face.predict_emotions(conference_of_interest, num_frames=num_frames)

# print(emotions_df)