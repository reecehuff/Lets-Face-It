#%% Imports
import os
import shutil
import glob
import numpy as np
import pandas as pd
import cv2
from tqdm import tqdm
from pytube import YouTube 
from datetime import datetime, timedelta
import pytz

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

def get_yt_upload_time(video_id):
    api_key = 'AIzaSyCrajdAuLe2HGh6X8ykBmzoGhlSFNc2uEk'
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.videos().list(
            part='snippet',
            id=video_id
        )
        response = request.execute()

        if 'items' in response and len(response['items']) > 0:
            video = response['items'][0]
            upload_timestamp = video['snippet']['publishedAt']
        else:
            print(f'Video with ID {video_id} not found.')
            upload_timestamp = None

    except HttpError as error:
        print(f'An error occurred: {error}')
        upload_timestamp = None
    
    # Process the upload_timestamp
    if upload_timestamp is None:
        assert upload_timestamp is not None, 'Unsuccessfully pulled the timestamp from the YouTube video'
    else: 
        # The timestamp returned by the YouTube Data API is in Coordinated Universal Time (UTC). 
        # The "Z" at the end of the timestamp string ("2021-07-23T18:16:00Z") stands for "Zulu time," which is another way of indicating UTC.
        utc_timestamp = datetime.fromisoformat(upload_timestamp.replace("Z", "+00:00"))
        target_timezone = "US/Eastern"  # Replace this with your desired timezone
        est_timezone = pytz.timezone(target_timezone)
        est_timestamp = utc_timestamp.astimezone(est_timezone)
        est_time_str = est_timestamp.strftime('%H:%M:%S')
        date_time_str = est_timestamp.strftime('%Y-%m-%d')
        timestamp_time_str = est_timestamp.strftime('%Y-%m-%d %H:%M:%S')
        timestamp = datetime.strptime(timestamp_time_str, '%Y-%m-%d %H:%M:%S')
        return date_time_str, est_time_str, timestamp

#%% A function for creating time stamps of the video given the start time and the seconds
def create_timestamps(start_time, seconds):
    from datetime import timedelta
    timestamps = []
    for s in seconds:
        dt = start_time + timedelta(seconds=s)
        timestamps.append(dt.strftime("%Y-%m-%d %H:%M:%S"))

    return timestamps

# A function for converting an mp4 to image frames 
def mp4_2_frames(video_path, save_freq, fps, start_time, frame_dir='data/frames/'):
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
    output_path = os.path.join(frame_dir, '%s' % date)
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
def save_identity_frames(excel_path='data/identity_frames.xlsx', save_path="data/identities_frames/"):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    identity_frames_excel = pd.read_excel(excel_path, index_col=0)
    for date, path in identity_frames_excel.iterrows():
        source = path['Identity Frame']
        target = os.path.join( save_path, date + "_" + os.path.basename(source) )
        shutil.copy(source, target)

#%% Define a simple function for getting the identity frame from the excel sheet from a date
def get_identity_frame_path(conference, indentity_frames=None):
    if indentity_frames is None:
        return None
    date = os.path.basename(conference)
    indentity_frame_path = indentity_frames.loc[date].values[0]
    return indentity_frame_path

#%% Define a function for processing the SPY data from https://www.kaggle.com/datasets/gratefuldata/intraday-stock-data-1-min-sp-500-200821
def process_SPY_data(input_spy_path, output_spy_path):

    # Read in the input CSV
    spy_data = pd.read_csv(input_spy_path, index_col=0)
    dates = spy_data["date"].to_list()
    # Convert their timestamps to cleaner timestamps
    timestamps = []
    for ts in dates:
        day, time = ts.split("  ")
        day = day[:4] + "-" + day[4:6] + "-" + day[6:]
        hour = time[:2]
        rest = time[2:]
        new_hour = str(int(hour)+2).zfill(2) # Convert to EST from MST
        timestamp = day + " " + new_hour + rest
        timestamps.append(timestamp)
    # Add the timestamps
    spy_data["timestamp"] = timestamps
    # Drop the date column
    spy_data = spy_data.drop(columns=['date'])
    # Sort the DataFrame by the timestamps
    spy_data = spy_data.sort_values(by=['timestamp'])
    # Set the timestamp as the index
    spy_data = spy_data.set_index('timestamp')
    # Write the output CSV
    spy_data.to_csv(output_spy_path)

#%% Define a function for returning a subDataFrame with all prices on that particular day
def get_intraday_prices(df, date):
    return df[(df.index >= '%s 00:00:00' % date) & (df.index <= '%s 23:59:59' % date)]

#%% Define a function for returning a Series with all volumes on that particular day
def get_intraday_volumes(df, date):
    prices = df[(df.index >= '%s 00:00:00' % date) & (df.index <= '%s 23:59:59' % date)]
    return prices['volume']

#%% Define a function for returning a Series with all returns on that particular day
def get_intraday_returns(df, date, price='close'):
    # Convert the date to datetime and get previous datetime days
    datetime_date = datetime.strptime(date, "%Y-%m-%d")
    datetime_prev_day = datetime_date - timedelta(days = 1)
    datetime_prev_10day = datetime_date - timedelta(days = 10)
    # Convert them to strings
    date = datetime_date.strftime("%Y-%m-%d")
    prev_day = datetime_prev_day.strftime("%Y-%m-%d")
    prev_10day = datetime_prev_10day.strftime("%Y-%m-%d")
    # Isolate the current day
    curr_day = df[(df.index >= '%s 00:00:00' % date) & (df.index <= '%s 23:59:59' % date)]
    # Isolate the 10 days before the previous day
    prev_days = df[(df.index >= '%s 00:00:00' % prev_10day) & (df.index <= '%s 23:59:59' % prev_day)]
    last_price = prev_days.iloc[-1:]
    prices_4_returns = pd.concat([last_price, curr_day])
    # Calculate the returns for the input price
    returns = prices_4_returns[price].pct_change().dropna()
    # Rename the Series
    returns = returns.rename('returns')
    # Convert to percentage
    returns = returns*100
    # Convert to basis points
    returns = returns*100

    # Return the returns 
    return returns

#%% Define a function for returning a DataFrame with all returns and volumes on that particular day
def get_intraday_returns_and_volumes(df, date, price='close'):
    # Isolate the returns on that particular date
    returns = get_intraday_returns(df, date, price)
    # Isolate the volume on that particular date
    volumes = get_intraday_volumes(df, date)
    # Merge the returns and volumes
    returns_and_volumes = pd.merge(returns, volumes, left_index=True, right_index=True)
    # Return the returns and volumes
    return returns_and_volumes

#%% Define a function that calculates the mean anger, disgust, and fear for a particular chairperson over all conferences
def get_mean_negative_emotions(emotions_base_dir):

    # Read in the excel file and isolate the dates associated with that particular fedchair
    excel_paths = sorted(glob.glob(os.path.join(emotions_base_dir, '*')))

    # NOTE: Need to delete this
    # excel_paths = ['data/emotions/2011-04-27.xlsx', 'data/emotions/2017-09-20.xlsx']

    # Initialize a DataFrame for all of the emotions
    all_emotions = pd.DataFrame()
    # Loop through the paths
    for path in excel_paths:
        # Verify that the path exists 
        assert os.path.exists(path), "%s does not exist" % path
        # Read in the emotions
        emotions = pd.read_excel(path, index_col=0)
        # Concatenate the DataFrame's together
        all_emotions = pd.concat([all_emotions, emotions])

    # Calculate the mean of the anger, disgust, and fear
    anger_mean   = all_emotions['angry'].mean()
    disgust_mean = all_emotions['disgust'].mean()
    fear_mean    = all_emotions['fear'].mean()
    negative_emotions_mean = anger_mean + disgust_mean + fear_mean

    # Calculate the std of the anger, disgust, and fear
    negative_emotions_std = all_emotions[['angry', 'disgust', 'fear']].sum(axis=1).std()

    # Calculate the PCA mean
    from sklearn.decomposition import PCA
    emotions_np = all_emotions.drop(columns='dominant_emotion').to_numpy()
    emotions_np = emotions_np[ ~np.isnan(emotions_np[:,0]) , :]
    pca = PCA(n_components=1)
    pc1 = pca.fit_transform(emotions_np).flatten()
    mean_pca = pc1.mean()

    # Return the mean negative emotion and the mean PCA
    return negative_emotions_mean, negative_emotions_std, mean_pca

#%% Define a function that calculates the mean anger, disgust, and fear for a particular chairperson over all conferences
def get_mean_negative_emotions_FOMC(path2excel, name, emotions_base_dir):

    # Read in the excel file and isolate the dates associated with that particular fedchair
    excel      = pd.read_excel(path2excel, 'QA_identifier')
    fedchairs  = excel['fedchair'].drop_duplicates()
    dates      = excel['date'].drop_duplicates()
    fedchairs_and_dates = excel.iloc[dates.index][['date', 'fedchair']].set_index('date').sort_index()
    chair_dates = fedchairs_and_dates[fedchairs_and_dates['fedchair'] == name]

    # Loop through those dates and save the excel paths associated with them 
    excel_paths = []
    for chair_date in chair_dates.index.to_list():
        excel_fn   = chair_date.strftime("%Y-%m-%d") + ".xlsx"
        excel_path = os.path.join(emotions_base_dir, excel_fn)
        excel_paths.append(excel_path)

    # NOTE: Need to delete this
    # excel_paths = ['data/emotions/2011-04-27.xlsx', 'data/emotions/2017-09-20.xlsx']

    # Initialize a DataFrame for all of the emotions
    all_emotions = pd.DataFrame()
    # Loop through the paths
    for path in excel_paths:
        # Verify that the path exists 
        assert os.path.exists(path), "%s does not exist" % path
        # Read in the emotions
        emotions = pd.read_excel(path, index_col=0)
        # Concatenate the DataFrame's together
        all_emotions = pd.concat([all_emotions, emotions])

    # Calculate the mean of the anger, disgust, and fear
    anger_mean   = all_emotions['angry'].mean()
    disgust_mean = all_emotions['disgust'].mean()
    fear_mean    = all_emotions['fear'].mean()
    negative_emotions_mean = anger_mean + disgust_mean + fear_mean

    # Calculate the std of the anger, disgust, and fear
    negative_emotions_std = all_emotions[['angry', 'disgust', 'fear']].sum(axis=1).std()

    # Calculate the PCA mean
    from sklearn.decomposition import PCA
    emotions_np = all_emotions.drop(columns='dominant_emotion').to_numpy()
    emotions_np = emotions_np[ ~np.isnan(emotions_np[:,0]) , :]
    pca = PCA(n_components=1)
    pc1 = pca.fit_transform(emotions_np).flatten()
    mean_pca = pc1.mean()

    # Return the mean negative emotion and the mean PCA
    return negative_emotions_mean, negative_emotions_std, mean_pca

#%% Define a function to gives the name of the fedchair given the date
def date_2_fedchair(path2excel, date):
    # Read in the excel file and isolate the dates associated with that particular fedchair
    excel      = pd.read_excel(path2excel, 'QA_identifier')
    fedchairs  = excel['fedchair'].drop_duplicates()
    dates      = excel['date'].drop_duplicates()
    fedchairs_and_dates = excel.iloc[dates.index][['date', 'fedchair']].set_index('date').sort_index()
    name = fedchairs_and_dates[fedchairs_and_dates.index == date]
    name = name['fedchair'].values[0]
    # Return the name of the fedchair
    return name

#%% Define a function for calculating the negative emotions variables
def negative_emotions_df(emotions, returns_and_volumes, date, neg_emotion_normalizers, frame_freq=2, compare_freq=3):

    # Initialize the output DataFrame
    output_df = pd.DataFrame()
    # Define the initial start time and desired_length
    start_time = emotions.index[0].split()[1]
    current_length = int(compare_freq * (60/frame_freq))
    desired_length = int(compare_freq * (60/frame_freq))
    # Loop through the DataFrame until the desired length is less than 90
    while current_length == desired_length:
        # Convert the date to datetime and get previous datetime days
        datetime_start_time = datetime.strptime(start_time, "%H:%M:%S") + timedelta(seconds=2) 
        datetime_next_3_min = datetime_start_time + timedelta(minutes = 2) + timedelta(seconds = 58)
        # Convert them to strings
        start_time = datetime_start_time.strftime("%H:%M:%S")
        next_3_min = datetime_next_3_min.strftime("%H:%M:%S")
        # Make them the full timestamp 
        start_time_timestamp = "%s %s" % (date, start_time)
        next_3_min_timestamp = "%s %s" % (date, next_3_min)
        # Isolate the portion of the DataFrame within these timestamps
        emotions_chunk = emotions[(emotions.index >= start_time_timestamp) & (emotions.index <= next_3_min_timestamp)]
        # Calculate the desired length
        current_length = len(emotions_chunk)
        if current_length != desired_length:
            break
        # Isolate the first and third minute timestamps
        first_minute  = emotions_chunk.index[29]
        third_minute  = emotions_chunk.index[89]
        # Isolate the returns and the volumes between the first and third minute
        returns_and_volumes_chunk = returns_and_volumes[(returns_and_volumes.index >= first_minute) & (returns_and_volumes.index <= third_minute)]
        # Calculate the mean return and mean volume
        mean_return = returns_and_volumes_chunk['returns'].mean()
        mean_volume = returns_and_volumes_chunk['volume'].mean()
        # Convert all of the emotions to a NumPy array and remove NaN's
        emotions_np = emotions_chunk.drop(columns='dominant_emotion').to_numpy()
        emotions_np = emotions_np[ ~np.isnan(emotions_np[:,0]) , :]
        # Isolate the negative emotions as a NumPy array and remove NaN's
        negative_emotions = emotions_chunk[['angry', 'disgust', 'fear']].to_numpy()
        negative_emotions = negative_emotions[ ~np.isnan(negative_emotions[:,0]) , :]
        # Calculate the mean negative emotion
        mean_neg_emotion = negative_emotions.sum(axis=1).mean()
        # Calculate the std negative emotion
        std_neg_emotion = negative_emotions.sum(axis=1).std()
        # Calculate the PCA negative emotion
        from sklearn.decomposition import PCA
        pca = PCA(n_components=1)
        pc1 = pca.fit_transform(emotions_np).flatten()
        pca_emotion = pc1.mean()
        # Define the output dictionary
        output_dict = {'timestamp': third_minute,
                    'return': mean_return,
                    'volume': mean_volume,
                    'mean_neg_emotion': mean_neg_emotion / neg_emotion_normalizers[0],
                    'std_neg_emotion': std_neg_emotion / neg_emotion_normalizers[1],
                    'pca_emotion': pca_emotion / neg_emotion_normalizers[2],
                    'dmd_neg_emotion': mean_neg_emotion - neg_emotion_normalizers[0]}
        # Append the output dictionary to the output DataFrame
        output_df = pd.concat([output_df, pd.DataFrame([output_dict])])
        # Update the start time 
        start_time = next_3_min
    # Set the index
    output_df = output_df.set_index('timestamp')
    # Return the output df
    return output_df