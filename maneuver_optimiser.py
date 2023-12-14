import pandas as pd
from data_paths import *

DEF_MANEUVERS = [
#   "2023-07-04T17:12:26"
    "2023-06-30T13:58:43",
    "2023-06-30T14:11:48",
    "2023-07-01T12:48:59",
    "2023-07-02T17:18:04",
    "2023-07-02T17:10:50",
    "2023-07-03T17:33:45",
    "2023-07-03T18:25:32"
]

def optimise_maneuvers(
        data_files: "list[str]", 
        maneuvers_timestamps: "list[str]", 
        output_folder: str = EXTRACTED_DATA_PATH, 
        best_maneuver_file_name: str = "best_maneuver.csv",
        best_in_out_file_name: str = "best_entry&exit.csv") -> None:
    '''
    This function will extract 2 maneuvers from the list given. 
    It will generate 2 csv files, one for the best maneuver (average speed over 2 mins around the given timestamp) and one for the best entry/exit average.
    '''
    data_frame = pd.DataFrame()
    maneuvers = pd.to_datetime(maneuvers_timestamps)
    print(maneuvers)

    for path in data_files:
        temp_df: pd.DataFrame = pd.read_csv(path)
        data_frame = pd.concat([data_frame, temp_df], axis=0, ignore_index=True)

    data_frame["timestamp"] = pd.to_datetime(data_frame['timestamp'])
    print("loaded all data!")
    print(data_frame)
    print(data_frame.dtypes)

    t_start = data_frame["timestamp"][0]
    t_end = data_frame["timestamp"][0]+pd.Timedelta("120 sec")
    best_avg = 0

    t_start_i = data_frame["timestamp"][0]
    t_end_o = data_frame["timestamp"][0]+pd.Timedelta("120 sec")
    best_avg_io = 0

    for man in maneuvers:
        print(f"checking man around {man}.")
        t_0 = man - pd.Timedelta("120s")

        while (t_0 < man):
            avg_out: pd.DataFrame = data_frame.loc[(data_frame["timestamp"] >= t_0) & (data_frame["timestamp"] <= t_0 + pd.Timedelta("120 sec"))]

            avg = 0
            div = 0
            for speed in avg_out["sog_kts"]:
                avg = avg + speed
                div = div + 1

            avg = avg/div
            avg_io = (avg_out["sog_kts"].iloc[0] + avg_out["sog_kts"].iloc[-1])/2

            if avg_io > best_avg_io:
                t_start_i = t_0
                t_end_o = t_0 + pd.Timedelta("120 sec")
                best_avg_io = avg_io
                print(f"new best avg io! {best_avg}")

            if avg > best_avg:
                t_start = t_0
                t_end = t_0 + pd.Timedelta("120 sec")
                best_avg = avg
                print(f"new best avg! {best_avg}")
            
            t_0 = avg_out["timestamp"].iloc[1]

    data_frame["timestamp"] = data_frame["timestamp"].map(lambda x: x.isoformat())

    output_data = data_frame.loc[(data_frame["timestamp"] >= t_start.isoformat()) & (data_frame["timestamp"] <= t_end.isoformat())]
    output_data_io = data_frame.loc[(data_frame["timestamp"] >= t_start_i.isoformat()) & (data_frame["timestamp"] <= t_end_o.isoformat())]
    output_data.to_csv(f"{output_folder}/{best_maneuver_file_name}")
    output_data_io.to_csv(f"{output_folder}/{best_in_out_file_name}")

if __name__ == "__main__":
    data_files = [f"{RAW_DATA_PATH}/{r_d}" for r_d in RAW_DATA]
    optimise_maneuvers(data_files, DEF_MANEUVERS)
    