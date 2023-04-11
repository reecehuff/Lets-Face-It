#%% Imports
import pandas as pd

#--Scripts
from core.plotter import Plotter

#%% Read in the final csv file of the mean_neg_emotion, std_neg_emotion, pca_emotion, and dmd_neg_emotion 

# You need to run process_emotions_and_returns.py with the same which_youtube_videos before running this script
which_youtube_videos = 'trump'

if which_youtube_videos == 'trump':
    #---Final path
    final_path = 'data/emotions_vs_returns/trump/returns_volumes_negative_emotions.csv'
    figures_path = "figures/trump"

elif which_youtube_videos == 'FOMC':
    #---Final path
    final_path = 'data/emotions_vs_returns/FOMC/returns_volumes_negative_emotions.csv'
    figures_path = "figures/FOMC"

else:
    raise "%s is a not a valid input to which_youtube_ids" % which_youtube_videos

df = pd.read_csv(final_path, index_col=0)

#%% Initialize the Plotter class
plotter = Plotter(figures_dir=figures_path)

#%% Plot the returns, volumes, and negative emotions

#-----------RETURNS-----------#
#---Returns vs. mean negative emotion
plotter.default_negative_emotions('', 'return', 'upper left')
plotter.negative_emotions(df, 'mean_neg_emotion', 'return', 'returns_vs_mean_neg_emotion.png')
#---Returns vs. std_neg_emotion
plotter.default_negative_emotions('std', 'return', 'lower left')
plotter.negative_emotions(df, 'std_neg_emotion', 'return', 'returns_vs_std_neg_emotion.png')
#---Returns vs. pca_emotion
plotter.default_negative_emotions('pca', 'return', 'upper left')
plotter.negative_emotions(df, 'pca_emotion', 'return', 'returns_vs_pca_emotion.png')
#---Returns vs. dmd_neg_emotion
plotter.default_negative_emotions('dmd', 'return', 'upper left')
plotter.negative_emotions(df, 'dmd_neg_emotion', 'return', 'returns_vs_dmd_neg_emotion.png')

#-----------VOLUMES-----------#
#---Returns vs. mean negative emotion
plotter.default_negative_emotions('', 'volume', 'upper right')
plotter.negative_emotions(df, 'mean_neg_emotion', 'volume', 'volumes_vs_mean_neg_emotion.png')
#---volumes vs. std_neg_emotion
plotter.default_negative_emotions('std', 'volume', 'lower right')
plotter.negative_emotions(df, 'std_neg_emotion', 'volume', 'volumes_vs_std_neg_emotion.png')
#---volumes vs. pca_emotion
plotter.default_negative_emotions('pca', 'volume', 'upper right')
plotter.negative_emotions(df, 'pca_emotion', 'volume', 'volumes_vs_pca_emotion.png')
#---volumes vs. dmd_neg_emotion
plotter.default_negative_emotions('dmd', 'volume', 'upper right')
plotter.negative_emotions(df, 'dmd_neg_emotion', 'volume', 'volumes_vs_dmd_neg_emotion.png')
