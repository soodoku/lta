from typing import List
import pandas as pd
import json
import pdb


def group_zips(data_path: str, diff: int, signal_strength: List):
    # 1. Filters out list of tv stations per zip code based on signal_strength
    df = pd.read_csv(data_path, dtype={"zipcode": str})
    header = set(df["callsign"].values)
    header = list(header)
    uni_zipcodes = set(df["zipcode"])
    uni_zipcodes = list(uni_zipcodes)
    data = {}
    for zipcode in uni_zipcodes:
        print(zipcode)
        row = []
        for col in header:
            inout = df[
                (df["zipcode"] == zipcode)
                & (df["callsign"] == col)
                & (df["signal_strength"].isin(signal_strength))
            ]
            if len(inout) > 0:
                if len(inout) == 1:
                    row.append(1)
                else:
                    print(inout)
            else:
                row.append(0)
        data[zipcode] = row
    return data


data_path = "./stations.csv"
signal_strength = [1, 2]
diff = 2
print(group_zips(data_path, diff, signal_strength))
# with open("ret.json", "w") as fp:
#     json.dump(group_zips(data_path, diff, signal_strength), fp)
