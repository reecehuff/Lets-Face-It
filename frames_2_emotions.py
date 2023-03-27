#%% Imports
import glob
import pandas as pd

#--Scripts
import core.utils as utils
import core.face as face

#%% Define the frames from the videos that will be used to verify the identity of the speaker
conferences = sorted(glob.glob('data/frames/*'))
# Define the frames in the video that will be used to identify the chair and save their paths to an excel file
identity_frames_excel_path = 'data/identity_frames.xlsx'
utils.get_identity_frames(conferences, save_path=identity_frames_excel_path)
# Save the identity frames to a new folder to verify they contain the chair
utils.save_identity_frames()

#%% Loop through the conferences and predict the emotions for all of the frames in the videos
indentity_frames = pd.read_excel(identity_frames_excel_path, index_col=0)
face.predict_all_emotions(indentity_frames, conferences)

#%% Debug one particular conference if the verification is struggling
# indentity_frames = pd.read_excel(identity_frames_excel_path, index_col=0)
# print(conferences)
# print(conferences[26])
# indentity_frame_path = indentity_frame_path = utils.get_identity_frame_path(indentity_frames, conferences[26])
# emotions_df = face.predict_emotions(conferences[26], indentity_frame_path, num_frames=100)
# print(emotions_df)