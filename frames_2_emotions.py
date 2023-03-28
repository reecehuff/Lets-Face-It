#%% Imports
import glob
import pandas as pd

#--Scripts
import core.utils as utils
import core.face as face

#%% Input toggle(s)
verify          = False # A toggle that if True will verify that the frame contains the chairperson
all_conferences = True  # A toggle that if True will apply DeepFace to all of the conferences

#%% Define the frames from the videos that will be used to verify the identity of the speaker
conferences = sorted(glob.glob('data/frames/*'))
# Define the frames in the video that will be used to identify the chair and save their paths to an excel file
identity_frames_excel_path = 'data/identity_frames.xlsx'
utils.get_identity_frames(conferences, save_path=identity_frames_excel_path)
# Save the identity frames to a new folder to verify they contain the chair
utils.save_identity_frames()

#%% Loop through the conferences and predict the emotions for all of the frames in the videos
if all_conferences:
    indentity_frames = pd.read_excel(identity_frames_excel_path, index_col=0)
    if verify:
        face.predict_all_emotions(conferences, indentity_frames)
    else:
        face.predict_all_emotions(conferences)

#%% Debug one particular conference if the verification is struggling
# indentity_frames = pd.read_excel(identity_frames_excel_path, index_col=0)
# conference_of_interest = conferences[0]
# num_frames = None
# print(conference_of_interest)
# if verify:
#     indentity_frame_path = utils.get_identity_frame_path(conference_of_interest, indentity_frames)
#     emotions_df = face.predict_emotions(conference_of_interest, indentity_frame_path, num_frames=num_frames)
# else:
#     emotions_df = face.predict_emotions(conference_of_interest, num_frames=num_frames)

# print(emotions_df)