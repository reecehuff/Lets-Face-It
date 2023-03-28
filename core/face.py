#%% Imports
from deepface import DeepFace
import os
import glob
import numpy as np
import pandas as pd
from tqdm import tqdm

#--Scripts
import core.utils as utils

#%% Define a function for predicting the emotions of an individual using DeepFace
def predict_emotion_from_image(img_path, truth_img_path=None, normalize=True):
    if truth_img_path is None:
        face_analysis = DeepFace.analyze(img_path = img_path, actions = ['emotion'], silent=True, enforce_detection=False)
    else:
        face_analysis = DeepFace.analyze(img_path = img_path, actions = ['emotion'], silent=True)
    emotion = face_analysis[0]['emotion']
    if normalize:
        total = sum(emotion.values())
        emotion = {k: v / total for k, v in emotion.items()}
    return emotion

#%% Define a function for return NaN emotions when the identity was not verified
def nan_emotions():
    return {'angry': np.NaN, 'disgust': np.NaN, 'fear': np.NaN, 'happy': np.NaN, 'sad': np.NaN, 'surprise': np.NaN, 'neutral': np.NaN, 'dominant_emotion': ''}

#%% Define a function for predicting the emotions of an individual using DeepFace
def verify_identity(truth_img_path, pred_img_path):
    if truth_img_path is None:
        return True
    try:
        result = DeepFace.verify(img1_path = truth_img_path, 
                                img2_path = pred_img_path, 
                                distance_metric = 'cosine',
                                model_name='Facenet'
        )
        return result['verified']
    except:
        return False
    
#%% Define a function for predicting all of the emotions and store them in an excel file 
def predict_emotions(conference, indentity_img_path=None, num_frames=None, save_path='data/emotions/'):

    # Create a path to save the save data only if that path does not already exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Get the frame_paths
    frame_paths = sorted(glob.glob(conference + '/*.png'))
    if num_frames is not None:
        frame_paths = frame_paths[:num_frames]
    # Initialize the emotions DataFrame
    emotions_df = pd.DataFrame()
    # Loop through the frames
    date = os.path.split(os.path.split(frame_paths[0])[0])[1]
    description = "Predicting emotions for frames in %s press conference" % date
    for frame in tqdm(frame_paths, desc=description, total=len(frame_paths)):
        # Verify the identity of the individual in the frame
        verify = verify_identity(indentity_img_path, frame)
        # Predict the emotions of the individual only if they are the chair (i.e., their identity has been verified)
        if verify:
            # Predict the emotions of the individual
            emotions = predict_emotion_from_image(frame, indentity_img_path)
            # Add the dominant emotion to the dictionary
            emotions['dominant_emotion'] = max(emotions, key=emotions.get)
        else:
            # Since their identity was not verified, we just return NaN's
            emotions = nan_emotions()
        # Add the timestamp to the emotions dictionary
        date = os.path.split(os.path.split(frame)[0])[1]
        time = os.path.basename(frame).replace(".png", "")
        emotions['timestamp'] = date + " " + time
        # Append the emotions dictionary to the end of the DataFrame
        emotions_df = emotions_df.append(emotions, ignore_index = True)
    # Set the index of the emotions DataFrame
    emotions_df = emotions_df.set_index('timestamp')

    # Save the DataFrame as an excel file
    date = os.path.basename(conference)
    excel_path = os.path.join(save_path, "%s.xlsx" % date)
    emotions_df.to_excel(excel_path)

    # Return the emotions DataFrame
    return emotions_df

#%% Define a function to loop through the conferences and predict the emotions for all of the frames
def predict_all_emotions(conferences, indentity_frames=None, num_frames=None, save_path='data/emotions/'):
    # Loop through the conferences
    description = "Predicting emotions for all conferences"
    for conference in tqdm(conferences, desc=description, total=len(conferences)):
        # Get the identity frame path 
        indentity_frame_path = utils.get_identity_frame_path(conference, indentity_frames)
        # Predict the emotions for all of the frames in the video
        predict_emotions(conference, indentity_frame_path, num_frames=num_frames, save_path=save_path)