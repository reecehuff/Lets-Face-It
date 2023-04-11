#%% Imports
import glob
import pandas as pd
import os

#--Scripts
import core.utils as utils

#%% Inputs
# You need to run frames_2_emotions.py with the same which_youtube_videos before running this script
which_youtube_videos = 'trump'

if which_youtube_videos == 'trump':
    #---Final directory and file name
    final_dir = 'data/emotions_vs_returns/trump'
    final_fn  = 'returns_volumes_negative_emotions.csv'
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    #---Paths related to emotions
    emotions_dir        = 'data/emotions/trump'
    emotion_excel_files = sorted(glob.glob(os.path.join(emotions_dir, '*')))
    yt_id_excel_path    = 'data/yt_ids/trump_yt_ids.xlsx'

elif which_youtube_videos == 'FOMC':
    #---Final directory and file name
    final_dir = 'data/emotions_vs_returns/FOMC'
    final_fn  = 'returns_volumes_negative_emotions.csv'
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    #---Paths related to emotions
    emotions_dir        = 'data/emotions/FOMC'
    emotion_excel_files = sorted(glob.glob(os.path.join(emotions_dir, '*')))
    yt_id_excel_path    = 'data/yt_ids/fomc_all.xlsx'

else:
    raise "%s is a not a valid input to which_youtube_ids" % which_youtube_videos

#---Paths related to financial data
spy_path = 'data/prices/SPY_1min_2008-2021.csv'
# Read in the process SPY intraday information
spy_data = pd.read_csv(spy_path, index_col=0)

#%% Loop through the excel files and calculate the negative emotion parameters

if which_youtube_videos == 'trump':

    # Initialize the final DataFrame
    final_df = pd.DataFrame()
    # Loop through the excel files
    for excel_file in emotion_excel_files:
        # Read in the emotions excel file
        emotions = pd.read_excel(excel_file, index_col=0)
        # Isolate the date from the emotions excel file
        date = emotions.index[0].split()[0]
        # Get the intraday returns and volumes on that particular date
        returns_and_volumes = utils.get_intraday_returns_and_volumes(spy_data, date)
        # Calculate the overall mean, the overall std, and the mean PCA for the particular chairperson
        overall_mean_neg_emotions, overall_std_neg_emotions, overall_mean_pca = utils.get_mean_negative_emotions(emotions_dir)
        neg_emotion_normalizers = [overall_mean_neg_emotions, overall_std_neg_emotions, overall_mean_pca]
        # Calculate and store the mean_neg_emotion, std_neg_emotion, pca_emotion, and dmd_neg_emotion in a DataFrame for that particular conference
        output_df = utils.negative_emotions_df(emotions, returns_and_volumes, date, neg_emotion_normalizers)
        # Concatenate the DataFrame to the final DataFrame
        final_df = pd.concat([final_df, output_df])
        # Print the name and date
        print(date)
    # Save the final DataFrame as a csv
    final_df.to_csv(os.path.join(final_dir, final_fn))

elif which_youtube_videos == 'FOMC':

    # Initialize the final DataFrame
    final_df = pd.DataFrame()
    # Loop through the excel files
    for excel_file in emotion_excel_files:
        # Read in the emotions excel file
        emotions = pd.read_excel(excel_file, index_col=0)
        # Isolate the date from the emotions excel file
        date = emotions.index[0].split()[0]
        # Get the intraday returns and volumes on that particular date
        returns_and_volumes = utils.get_intraday_returns_and_volumes(spy_data, date)
        # Get the name of the chair person given the date of the conference
        name = utils.date_2_fedchair(yt_id_excel_path, date)
        # Calculate the overall mean, the overall std, and the mean PCA for the particular chairperson
        overall_mean_neg_emotions, overall_std_neg_emotions, overall_mean_pca = utils.get_mean_negative_emotions_FOMC(yt_id_excel_path, name, emotions_dir)
        neg_emotion_normalizers = [overall_mean_neg_emotions, overall_std_neg_emotions, overall_mean_pca]
        # Calculate and store the mean_neg_emotion, std_neg_emotion, pca_emotion, and dmd_neg_emotion in a DataFrame for that particular conference
        output_df = utils.negative_emotions_df(emotions, returns_and_volumes, date, neg_emotion_normalizers)
        # Concatenate the DataFrame to the final DataFrame
        final_df = pd.concat([final_df, output_df])
        # Print the name and date
        print(date)
        print(name)
    # Save the final DataFrame as a csv
    final_df.to_csv(os.path.join(final_dir, final_fn))