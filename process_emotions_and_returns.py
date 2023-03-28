#%% Imports
import glob
import pandas as pd
import os

#--Scripts
import core.utils as utils

#%% Inputs
base_dir = 'data/emotions'
excel_files = sorted(glob.glob(os.path.join(base_dir, '*')))
path2excel = 'TVOMP/Main/data/raw/fomc_all.xlsx'
final_dir = 'data/emotions_vs_returns'
final_fn  = 'returns_volumes_negative_emotions.csv'
if not os.path.exists(final_dir):
    os.makedirs(final_dir)

#%% Gather and process the SPY data as needed
# Define the input and output paths to the SPY data
input_spy_path  = 'data/prices/1_min_SPY_2008-2021.csv'
output_spy_path = 'data/prices/processed_1_min_SPY_2008-2021.csv'
# Process the SPY data only if the output file has not already been written 
if not os.path.exists(output_spy_path):
    utils.process_SPY_data(input_spy_path, output_spy_path)
# Read in the process SPY intraday information
spy_data = pd.read_csv(output_spy_path, index_col=0)

#%% Loop through the excel files and calculate the negative emotion parameters
# Initialize the final DataFrame
final_df = pd.DataFrame()
# Loop through the excel files
for excel_file in excel_files:
    # Read in the emotions excel file
    emotions = pd.read_excel(excel_file, index_col=0)
    # Isolate the date from the emotions excel file
    date = emotions.index[0].split()[0]
    # Get the intraday returns and volumes on that particular date
    returns_and_volumes = utils.get_intraday_returns_and_volumes(spy_data, date)
    # Get the name of the chair person given the date of the conference
    name = utils.date_2_fedchair(path2excel, date)
    # Calculate the overall mean, the overall std, and the mean PCA for the particular chairperson
    overall_mean_neg_emotions, overall_std_neg_emotions, overall_mean_pca = utils.get_mean_negative_emotions(path2excel, name, base_dir)
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