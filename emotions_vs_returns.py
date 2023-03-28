#%% Imports
import pandas as pd

#--Scripts
from core.plotter import Plotter

#%% Initialize the Plotter class
plotter = Plotter()

#%% Read in the final csv file of the mean_neg_emotion, std_neg_emotion, pca_emotion, and dmd_neg_emotion 
df = pd.read_csv('data/emotions_vs_returns/returns_volumes_negative_emotions.csv', index_col=0)
print(df)

#%% Plot the returns, volumes, and negative emotions

#-----------RETURNS-----------#
#---Returns vs. mean negative emotion
plotter.default_negative_emotions('return', '', 'upper left')
plotter.negative_emotions(df,'return', 'mean_neg_emotion', 'returns_vs_mean_neg_emotion.png')
#---Returns vs. std_neg_emotion
plotter.default_negative_emotions('return', 'std', 'lower left')
plotter.negative_emotions(df,'return', 'std_neg_emotion', 'returns_vs_std_neg_emotion.png')
#---Returns vs. pca_emotion
plotter.default_negative_emotions('return', 'pca', 'upper left')
plotter.negative_emotions(df,'return', 'pca_emotion', 'returns_vs_pca_emotion.png')
#---Returns vs. dmd_neg_emotion
plotter.default_negative_emotions('return', 'dmd', 'upper left')
plotter.negative_emotions(df,'return', 'dmd_neg_emotion', 'returns_vs_dmd_neg_emotion.png')

#-----------VOLUMES-----------#
#---Returns vs. mean negative emotion
plotter.default_negative_emotions('volume', '', 'upper right')
plotter.negative_emotions(df,'volume', 'mean_neg_emotion', 'volumes_vs_mean_neg_emotion.png')
#---volumes vs. std_neg_emotion
plotter.default_negative_emotions('volume', 'std', 'lower right')
plotter.negative_emotions(df,'volume', 'std_neg_emotion', 'volumes_vs_std_neg_emotion.png')
#---volumes vs. pca_emotion
plotter.default_negative_emotions('volume', 'pca', 'upper right')
plotter.negative_emotions(df,'volume', 'pca_emotion', 'volumes_vs_pca_emotion.png')
#---volumes vs. dmd_neg_emotion
plotter.default_negative_emotions('volume', 'dmd', 'upper right')
plotter.negative_emotions(df,'volume', 'dmd_neg_emotion', 'volumes_vs_dmd_neg_emotion.png')
