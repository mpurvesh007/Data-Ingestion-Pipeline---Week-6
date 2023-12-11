# File Reading and Data Processing
Introduction
This task involves reading a large CSV/text file (2+ GB) and exploring different methods of file reading for computational efficiency. The file is read using Pandas, Dask, Modin, and Ray. Basic validation is performed on data columns, and the results are summarized. Additionally, a YAML configuration file is created to store column names and other details.

# Dataset Link - https://www.kaggle.com/datasets/elemento/nyc-yellow-taxi-trip-data 
1. Data set size - 2.0 GB

# File Reading Approaches
1. Pandas
Pandas was used to read the file, taking approximately 1 minute and 16 seconds.

2. Dask
Dask, a parallel computing library, performed the file reading in approximately 211 milliseconds.

3. Modin
Modin, which aims to provide fast DataFrame processing, encountered a memory issue and did not complete successfully.

4. Ray
Ray, a distributed computing framework, is not available for DataFrame operations in this environment.

# Basic Data Validation
Basic validation was performed on data columns, including removing special characters and white spaces from the column names. Column name and length validation passed.

# YAML Configuration
A YAML configuration file was created to store file details such as file type, dataset name, delimiter, and column names.

# Number of Columns and Column Name Validation
Validation was performed to ensure the number of columns and column names match between the ingested file and the YAML configuration.

# Writing File
The processed data was written to a pipe-separated text file (|) in gz format.

# File Summary
The final processed file contains:



Total number of rows: 13,351,609
Total number of columns: 19
File size: 516.63 MB

# Conclusion
Dask demonstrated superior performance in file reading compared to Pandas.
Modin encountered memory issues, and Ray was not available for DataFrame operations.
Basic data validation and YAML configuration were successfully performed.
The final processed file is in pipe-separated text format with gzip compression (2 GB file compressed to 516.63 MB).
