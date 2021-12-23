from typing import List
import pandas as pd
import json
import pdb


def group_zips(data_path: str, diff: int, signal_strength: List):
    # 1. Filters out list of tv stations per zip code based on signal_strength
    df = pd.read_csv(data_path)
    station_per_zip_code_data = {}
    for row in df.values:
        if row[5] in signal_strength:
            if row[0] in station_per_zip_code_data.keys():
                station_per_zip_code_data[row[0]].append([row[1], row[5]])
            else:
                station_per_zip_code_data[row[0]] = [[row[1], row[5]]]
    # 3. For each zip code, finds all zip codes where overlap between list of tv stations is as large as `diff`
    per_zip_code_diff_range_data = {}
    for zipcode1, stations in station_per_zip_code_data.items():
        for zipcode2 in range(zipcode1 - diff, zipcode1 + 1 + diff):
            if zipcode1 in per_zip_code_diff_range_data.keys():
                try:
                    per_zip_code_diff_range_data[zipcode1] = (
                        per_zip_code_diff_range_data[zipcode1]
                        + station_per_zip_code_data[zipcode2]
                    )
                except KeyError:
                    pass
            else:
                try:
                    per_zip_code_diff_range_data[zipcode1] = station_per_zip_code_data[
                        zipcode2
                    ]
                except KeyError:
                    pass
    return {
        "station_per_zip_code_data": station_per_zip_code_data,
        "per_zip_code_diff_range_data": per_zip_code_diff_range_data,
    }


data_path = "./stations.csv"
signal_strength = [1, 2, 3]
diff = 2
with open("ret.json", "w") as fp:
    json.dump(group_zips(data_path, diff, signal_strength), fp, indent=4)
