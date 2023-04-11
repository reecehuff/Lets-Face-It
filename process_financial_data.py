#%% Imports
import pandas as pd
import os

#--Scripts
import core.utils as utils

#%% Gather and process the SPY data as needed
# Define the input and output paths to the SPY data
input_spy_path  = 'data/prices/raw/raw_1_min_SPY_2008-2021.csv'
output_spy_path = 'data/prices/SPY_1min_2008-2021.csv'
# Process the SPY data only if the output file has not already been written 
if not os.path.exists(output_spy_path):
    utils.process_SPY_data(input_spy_path, output_spy_path)
# Read in the process SPY intraday information
spy_data = pd.read_csv(output_spy_path, index_col=0)
# Print the processed SPY data
print(spy_data)