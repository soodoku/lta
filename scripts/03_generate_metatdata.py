from pandas import read_csv

data = []
with open("../output.log", "r") as fp:
    for x in fp.readlines():
        if not x.startswith("{'"):
            data.append(x[:-1])

code_set_list = list(
    set(list(read_csv("../stations.csv", dtype={"zipcode": str})["zipcode"]))
)

no_data_but_log = []
for x in data:
    if x not in code_set_list:
        no_data_but_log.append(x)


all_code_set_list = list(
    set(list(read_csv("../data/us_zipcodes.csv", dtype={"zip_code": str})["zip_code"]))
)
no_data_no_log = []
for x in all_code_set_list:
    if x in code_set_list or x in no_data_but_log:
        pass
    else:
        no_data_no_log.append(x)
print(f"all zip codes_give:{len(all_code_set_list)}")
print(f"data found for codes:{len(code_set_list)}")
print(f"log found but data not found:{len(no_data_but_log)}")
print(f"no dtata and no log {len(no_data_no_log)}")
