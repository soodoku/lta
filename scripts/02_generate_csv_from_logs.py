import ast
import csv

data = []
with open("../output.log", "r") as fp:
    for x in fp.readlines():
        if x.startswith("{'"):
            temp = ast.literal_eval(x)
            data.append(temp)
keys = data[0].keys()

with open("../stations.csv", "w", newline="") as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)
