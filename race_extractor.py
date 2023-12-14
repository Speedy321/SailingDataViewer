import pandas as pd
import argparse

from data_paths import EXTRACTED_DATA_PATH

def extract_race(
    data_file_path: str, 
    race_name: str,
    start_timestamp: str,
    end_timestamp: str,
    output_folder: str = EXTRACTED_DATA_PATH
):
    data_file: pd.DataFrame = pd.read_csv(data_file_path)
    t_start = f"{data_file['timestamp'][0].split('T')[0]}T{start_timestamp}"
    t_end = f"{data_file['timestamp'][0].split('T')[0]}T{end_timestamp}"

    out_data: pd.DataFrame = data_file.loc[(data_file["timestamp"] >= t_start) & (data_file["timestamp"] <= t_end)]
    out_data.to_csv(f"{output_folder}/{race_name}.csv")

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("file")
    arg_parser.add_argument("race_name")
    arg_parser.add_argument("start")
    arg_parser.add_argument("end")

    args = arg_parser.parse_args()

    extract_race(args.file, args.race_name, args.start, args.end)