import csv
import glob
import os

def count_rows_in_csv(file_path):
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        row_count = sum(1 for row in reader)  # Count each row in the reader
    row_count -= 1  # Subtract 1 to account for the header row
    return row_count

def count_rows_in_all_csvs(directory_path):
    # Construct the pattern to match all CSV files in the directory
    pattern = os.path.join(directory_path, '*.csv')
    # Use glob to find all files matching the pattern
    csv_files = glob.glob(pattern)
    
    # Iterate over each file and print the number of rows
    for file_path in csv_files:
        number_of_rows = count_rows_in_csv(file_path)
        print(f'{os.path.basename(file_path)}: {number_of_rows}')

directory_path = './'  # Replace with your directory path to csv files
count_rows_in_all_csvs(directory_path)
