import argparse
import os

from data_paths import *
from maneuver_optimiser import optimise_maneuvers
from map_gen import generate_map
from race_extractor import extract_race
from speed_finder import extract_speeds

def list_dirs(root_dir: str) -> list[str]:
    files = []
    for file in os.listdir(args.folder):
        dir = os.path.join(args.folder, file)
        if os.path.isdir(dir):
            files.extend(list_dirs(dir))
        else:
            files.append(dir)
    return files


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", action="append", help="Path to a data CSV file to load. Can be repeated.", default=([f"{RAW_DATA_PATH}/{rd}" for rd in RAW_DATA]+[f"{EXTRACTED_DATA_PATH}/{ed}"for ed in EXTRACTED_DATA]))
    parser.add_argument("--folder", action="append", help="Path to a folder containing CSV files to load. Will load all files from the folder", default=None)
    parser.add_argument("-n", "--nogen", action="store_true", help="Do not generate the map. To be used with options asking for extracting specific data.")
    parser.add_argument("-r", "--race", action="append", nargs=3, help="Extract the race according to the provided info. [-r <name> <start_timestamp> <end_timestamp>]. Can be repeated.")
    parser.add_argument("-s", "--speeds", action="store_true", help="Extract the optimal speeds to files for best point, best 10 sec and best 2 mins.")
    parser.add_argument("-m", "--maneuvers", action="append", help="Extract the best 2 minutes average speed and entry/exit speed around the provided timestamp. Can be repeated to extract the best from a list of maneuvers.")
    parser.add_argument("--name", help="Map name, default: [Foiling Week 2023 - Rafale 3.5]", default="Foiling Week 2023 - Rafale 3.5")

    args = parser.parse_args()

    files = args.files    
    if args.folder:
        files.extend(list_dirs(args.folder))
    
    if not args.nogen:
        generate_map(args.name, files)
    
    
    
