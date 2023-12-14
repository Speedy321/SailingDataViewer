import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from colors import CSS_COLORS
from data_paths import *

def generate_map(map_name: str, data_paths: "list[str]") -> None:
    '''
    This function generates a map (plotly mapbox) and displays it with the default renderer for your device, probably the web browser.
    It takes the name of the generated map and a list of paths to the data csv files to load the data from. 1 file per run or similar. It will color the data from each file differently.
    '''
    dataframes: 'list[pd.DataFrame]' = []
    figures: 'list[go.Figure]' = []
    for i in range(len(data_paths)):
        dataframes.append(pd.read_csv(data_paths[i]))
        figures.append(
            px.scatter_mapbox(
                dataframes[i], 
                lat='latitude', 
                lon='longitude',
                hover_name='timestamp', 
                hover_data=['sog_kts', 'hdg_true'],
                mapbox_style='open-street-map', 
                center={"lat":45.79597317443749, "lon":10.832164643194206}, 
                zoom=16,
                color_discrete_sequence=[CSS_COLORS[i]]
            )
        )
        figures[i]["data"][0]["showlegend"] = True
        name = data_paths[i].split("/")[-1].replace("_", '.').split(".")
        figures[i]["data"][0]["name"] = f"{name[0]} {name[1]}"
        if i > 0:
            figures[0].add_traces(figures[i].data)

    figures[0].update_layout(title = map_name, title_x=0.5, showlegend=True)
    figures[0].show()

if __name__ == "__main__":
    data = [f"{RAW_DATA_PATH}/{raw_d}" for raw_d in RAW_DATA]
    data += [f"{EXTRACTED_DATA_PATH}/{ext_d}" for ext_d in EXTRACTED_DATA]
    print(data)
    generate_map(f'FVM - Foiling week - Rafale 3.5', data)