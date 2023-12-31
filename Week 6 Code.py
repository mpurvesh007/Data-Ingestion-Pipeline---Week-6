# -*- coding: utf-8 -*-
"""cab_data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tN89ZVt-ucFBTXKgsRpjUN8CPFXXeTql

# 1. Installing Required Library
"""

!pip install dask
!pip install modin[all]
!pip install ray

import pandas as pd
import dask.dataframe as dd
import modin.pandas as mpd
import ray
ray.init()
import os

"""# 2. Mounting Google drive to read the file stored in drive directly"""

from google.colab import drive
drive.mount('/content/drive')

# Defining the file path from google drive
file_path = '/content/drive/MyDrive/yellow_tripdata_2015-03.csv'

"""# 3. Different methods of file reading Dask, Modin, Ray, pandas and presenting  the findings in terms of reading time"""

# Commented out IPython magic to ensure Python compatibility.
# Print time taken by Pandas to read the file
# %time df_pandas = pd.read_csv(file_path)

# print first 5 rows of dataframe
df_pandas.head()

# Commented out IPython magic to ensure Python compatibility.
# performing reading of file using dask
import dask.dataframe as dd

# Measure time taken by Dask to read the file
# %time df_dask = dd.read_csv(file_path)

import dask.dataframe as dd

# Specify dtype for 'extra' and 'tolls_amount'
dtype_spec = {'extra': 'float64', 'tolls_amount': 'float64'}

# Read CSV with explicit dtype specification
df_dask = dd.read_csv(file_path, assume_missing=True, dtype=dtype_spec)

# Displaying the first few 5 row
df_dask.head()

# Commented out IPython magic to ensure Python compatibility.
import modin.pandas as mpd

# Find time taken by Modin to read the file
# %time df_modin = mpd.read_csv(file_path)

# Commented out IPython magic to ensure Python compatibility.
import ray.dataframe as rd

ray.init()

# Record the time taken by Ray
# %time df_ray = rd.read_csv(file_path)

ray.shutdown()

import matplotlib.pyplot as plt

# Execution times
pandas_time = 1 * 60 + 1  # 1 minute and  1 seconds
dask_time = 0.186  # 186 milliseconds

# Create a bar plot
labels = ['Pandas', 'Dask']
times = [pandas_time, dask_time]

plt.bar(labels, times, color=['blue', 'orange'])
plt.ylabel('Execution Time (seconds)')
plt.title('Computational Efficiency: Pandas vs Dask')
plt.show()

df_pandas.info()

"""# 4. create a YAML file and write the column name in YAML file while defining separator of read and write file, column name in YAML


"""

yaml_config = """
file_type: csv
dataset_name: mydataset
file_name: file_path
table_name: mytable
inbound_delimiter: ","
outbound_delimiter: "|"
skip_leading_rows: 1
columns:
    - VendorID
    - tpep_pickup_datetime
    - tpep_dropoff_datetime
    - passenger_count
    - trip_distance
    - pickup_longitude
    - pickup_latitude
    - RateCodeID
    - store_and_fwd_flag
    - dropoff_longitude
    - dropoff_latitude
    - payment_type
    - fare_amount
    - extra
    - mta_tax
    - tip_amount
    - tolls_amount
    - improvement_surcharge
    - total_amount
"""


# Define the directory path
directory_path = '/content/drive/MyDrive/path/to/'

# Create the directory if it doesn't exist
os.makedirs(directory_path, exist_ok=True)

# Save YAML configuration to a file
yaml_file_path = os.path.join(directory_path, 'config.yaml')
with open(yaml_file_path, 'w') as file:
    file.write(yaml_config)

# Print the path where the YAML file is saved for further analysis
print(f"YAML file saved to: {yaml_file_path}")

from testutility import read_config_file

"""# 5.Validate number of columns and column name of ingested file with YAML."""

# Import necessary libraries
import logging
import os
import subprocess
import yaml
import pandas as pd
import datetime
import gc
import re

# Function to read a YAML configuration file
def read_config_file(filepath):
    with open(filepath, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.error(exc)

# Function to replace consecutive occurrences of a character in a string
def replacer(string, char):
    pattern = char + '{2,}'
    string = re.sub(pattern, char, string)
    return string

# Function to validate column names in a DataFrame against expected configuration
def col_header_val(df, table_config):
    '''
    Replace whitespaces in the column
    and standardize column names
    '''
# Convert column names to lowercase and replace non-word characters with underscores
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace('[^\w]', '_', regex=True)
    df.columns = list(map(lambda x: x.strip('_'), list(df.columns)))
    df.columns = list(map(lambda x: replacer(x, '_'), list(df.columns)))

# Extract and sort expected column names from the configuration
    expected_col = list(map(lambda x: x.lower(), table_config['columns']))
    expected_col.sort()

# Standardize DataFrame column names
    df.columns = list(map(lambda x: x.lower(), list(df.columns)))
    df = df.reindex(sorted(df.columns), axis=1)
    # Validate column names and lengths
    if len(df.columns) == len(expected_col) and list(expected_col) == list(df.columns):
        print("Column name and column length validation passed")
        return 1
    else:
        print("Column name and column length validation failed")
        mismatched_columns_file = list(set(df.columns).difference(expected_col))
        print("Following File columns are not in the YAML file", mismatched_columns_file)
        missing_YAML_file = list(set(expected_col).difference(df.columns))
        print("Following YAML columns are not in the file uploaded", missing_YAML_file)
        return 0

# Load YAML configuration
yaml_file_path = '/content/drive/MyDrive/path/to/config.yaml'
with open(yaml_file_path, 'r') as stream:
    try:
        table_config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logging.error(exc)

# Validate columns
col_header_val_result = col_header_val(df_pandas, table_config)

"""# 6. Write the file in pipe separated text file (|) in gz format.
# 7. Create a summary of the file:

## Total number of rows,

## Total number of columns

## File size


"""

# Write the file in pipe-separated text file (|) in gz format
output_file_path = os.path.join(directory_path, 'output_file.gz')
df_pandas.to_csv(output_file_path, sep='|', compression='gzip', index=False)

# Create a summary of the file
total_rows = df_pandas.shape[0]
total_columns = df_pandas.shape[1]
file_size = os.path.getsize(output_file_path) / (1024 * 1024)  # Convert to MB

print(f"Total number of rows: {total_rows}")
print(f"Total number of columns: {total_columns}")
print(f"File size: {file_size:.2f} MB")