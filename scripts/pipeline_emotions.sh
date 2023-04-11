#!/bin/bash

# Toggles 
toggle_yt_2_frames="on"
toggle_frames_2_emotions="on"
toggle_process_financial_data="on"
toggle_process_emotions_and_returns="on"
toggle_emotions_vs_returns="on"

# Function for running a Python script
function run_python_script() {
  echo " "
  echo "=============================================="
  echo "   Running $1"
  echo "=============================================="
  echo " "
  python "$1"
}

# ====================== #
# === yt_2_frames.py === #
# ====================== #
# ---- Description ----- #
# Script for downloading YouTube videos and converting them to frames 

#---Inputs: 
#   - excel file with YouTube ID's and upload date
#       -> stored in data/yt_ids
#---Outputs: 
#   - mp4 files of the YouTube videos 
#       -> stored in data/mp4s
#   - frames (png image files) stored 
#       -> stored in data/frames
if [[ $toggle_yt_2_frames == "on" ]]; then
  run_python_script yt_2_frames.py
fi


# ============================ #
# === frames_2_emotions.py === #
# ============================ #
# -------- Description ------- #
# Script for predicting the emotions of the faces in the frames from the previous step (data/frames)

#---Inputs: 
#   - 
#---Outputs: 
#   - excel files with the predicted emotion state for each frame
#       -> stored in data/emotions
if [[ $toggle_frames_2_emotions == "on" ]]; then
  run_python_script frames_2_emotions.py
fi


# ================================= #
# === process_financial_data.py === #
# ================================= #
# ----------- Description --------- #
# Script for processing the finanical data

#---Inputs: 
#   - path(s) to files raw financial intraday data
#---Outputs: 
#   - excel files with processed finanical data
if [[ $toggle_process_financial_data == "on" ]]; then
  run_python_script process_financial_data.py
fi


# ======================================= #
# === process_emotions_and_returns.py === #
# ======================================= #
# -------------- Description ------------ #
# Script for processing the emotions and the intraday returns on those days

#---Inputs: 
#   - path to the emotions excel files from the previous step
#       -> default is data/emotions
#   - path to financial excel files 
#       -> default is data/prices
#---Outputs: 
#   - excel file with the distilled emotion (e.g., negative emotions) and finance metrics (e.g., returns and volumes) from those time stamps
#       -> stored in data/emotions_vs_returns
# run_python_script process_emotions_and_returns.py
if [[ $toggle_process_emotions_and_returns == "on" ]]; then
  run_python_script process_emotions_and_returns.py
fi


# ============================== #
# === emotions_vs_returns.py === #
# ============================== #
# --------- Description -------- #
# Script for performing linear regression between the emotional states and financial metrics from the previous step

#---Inputs: 
#   - path to the excel file containing the distilled emotion and finance metrics from the previous step
#       -> default is 'data/emotions_vs_returns/returns_volumes_negative_emotions.csv'
#---Outputs: 
#   - figures of the correlation between all of the independent and dependent variables
#       -> stored in figures directory
if [[ $toggle_emotions_vs_returns == "on" ]]; then
  run_python_script emotions_vs_returns.py
fi





# Final print
echo " "