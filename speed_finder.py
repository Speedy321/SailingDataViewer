import pandas as pd
from data_paths import *

def extract_speeds(
    data_paths: "list[str]",
    output_folder: str = EXTRACTED_DATA_PATH,
    best_avg_file_name: str = "best_avg.csv",
    best_10s_file_name: str = "best_10sec.csv",
    max_speed_file_name: str = "max_speed.csv"    
):
    data_frame = pd.DataFrame()

    for path in data_paths:
        data_file: pd.DataFrame = pd.read_csv(path)
        data_frame = pd.concat([data_frame, data_file], axis=0, ignore_index=True)

    data_frame["timestamp"] = pd.to_datetime(data_frame['timestamp'])
    print("loaded all data!")
    print(data_frame)
    print(data_frame.dtypes)

    t_start = data_frame["timestamp"][0]
    t_end = data_frame["timestamp"][0]+pd.Timedelta("120 sec")
    best_avg = 0

    t_10s_start = data_frame["timestamp"][0]
    t_10s_end = data_frame["timestamp"][0]+pd.Timedelta("120 sec")
    best_10s_avg = 0

    t_single = data_frame["timestamp"][0]
    single_max = 0

    for stamp in data_frame["timestamp"]:
        temp_out = data_frame.loc[(data_frame["timestamp"] >= stamp) & (data_frame["timestamp"] <= stamp + pd.Timedelta("120 sec"))]
        temp_10s = data_frame.loc[(data_frame["timestamp"] >= stamp) & (data_frame["timestamp"] <= stamp + pd.Timedelta("10 sec"))]
        #print(temp_out["sog_kts"])

        if temp_out["sog_kts"].iloc[0] > single_max:
            single_max = temp_out["sog_kts"].iloc[0]
            t_single = stamp
            print(f"new single max! {single_max} {stamp}")

        avg = 0
        div = 0
        for speed in temp_out["sog_kts"]:
            avg = avg + speed
            div = div + 1
        avg = avg/div

        if avg > best_avg:
            t_start = stamp
            t_end = stamp + pd.Timedelta("120 sec")
            best_avg = avg
            print(f"new best avg! {best_avg}")

        avg_10s = 0
        div_10s = 0
        for speed in temp_10s["sog_kts"]:
            avg_10s = avg_10s + speed
            div_10s = div_10s + 1

        avg_10s = avg_10s/div_10s
        #print(f"{avg}, {avg_10s}")

        if avg_10s > best_10s_avg:
            t_10s_start = stamp
            t_10s_end = stamp + pd.Timedelta("10 sec")
            best_10s_avg = avg_10s
            print(f"new best 10sec avg! {best_10s_avg}")
            #print(temp_10s)


    data_frame["timestamp"] = data_frame["timestamp"].map(lambda x: x.isoformat())

    output_data = data_frame.loc[(data_frame["timestamp"] >= t_start.isoformat()) & (data_frame["timestamp"] <= t_end.isoformat())]
    sing_out = data_frame.loc[(data_frame["timestamp"] == t_single.isoformat())]
    avg_10s_out = data_frame.loc[(data_frame["timestamp"] >= t_10s_start.isoformat()) & (data_frame["timestamp"] <= t_10s_end.isoformat())]

    output_data.to_csv(f"{output_folder}/{best_avg_file_name}")
    sing_out.to_csv(f"{output_folder}/{max_speed_file_name}")
    avg_10s_out.to_csv(f"{output_folder}/{best_10s_file_name}")

if __name__ == "__main__":
    files = [f"{RAW_DATA_PATH}/{path}" for path in RAW_DATA]
    extract_speeds(files)