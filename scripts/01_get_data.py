from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
import json
import pdb

df = pd.read_csv("./data/us_zipcodes.csv")
zip_code = list(df["zip_code"])
# used driver on this link https://chromedriver.storage.googleapis.com/94.0.4606.41/chromedriver_linux64.zip
browser = webdriver.Chrome("./chromedriver")
browser.get("https://www.fcc.gov/media/engineering/dtvmaps")
input_box = browser.find_element(By.CLASS_NAME, "map-address-container")
input_box = input_box.find_element(By.TAG_NAME, "form")
input_box = input_box.find_element(By.ID, "startpoint")
for x in zip_code:
    print(x)
    input_box.clear()
    input_box.send_keys(x)
    time.sleep(2)
    browser.find_element(By.ID, "btnSub").click()
    time.sleep(10)
    # save page
    try:
        source = browser.page_source
    except:
        print(x, "address not found")
        continue
    with open(f"webpages/{x}.html", "w") as fp:
        fp.write(source)
    # scrape data
    # frist get table having data
    soup = BeautifulSoup(browser.page_source, "html.parser")
    table_soup = soup.find("div", {"id": "contourdata"})
    tables = table_soup.find_all("table")
    try:
        data_table = tables[2]
    except:
        continue
    # get rows
    data_table = data_table.find("tbody")
    page_data = []
    for strength in [1, 2, 3, 4]:
        try:
            data_table_in = data_table.find_all("tr", {"class": f"strength{strength}"})
        except AttributeError:
            continue
        for row in data_table_in:
            st = re.findall(r'onclick="getdetail(.*)" style="', str(row))
            Facility_ID = re.findall(r"Facility ID:\d*", str(st))
            station = {
                "zipcode": x,
                "callsign": row.find_all("td")[1].text.replace("\n", ""),
                "network": row.find_all("td")[2]
                .text.replace("\n", "")
                .replace(" ", ""),
                "channel_number": row.find_all("td")[3]
                .text.replace("\n", "")
                .replace(" ", ""),
                "band": row.find_all("td")[4].text.replace("\n", "").replace(" ", ""),
                "signal_strength": strength,
                "facility_id": re.search(r"Facility ID: \d*", str(st))
                .group(0)
                .replace("Facility ID: ", ""),
                "rx_strength": re.search(
                    r"RX Strength: \d* [a-z-A-Z]*\/[a-z]*", str(st)
                )
                .group(0)
                .replace("RX Strength: ", ""),
                "tower_distance": re.search(r"Tower Distance: .*; ", str(st))
                .group(0)
                .replace("Tower Distance: ", "")
                .replace("; ", ""),
            }
            try:
                station["ia"] = row.find_all("td")[5].text[:1]
            except:
                station["ia"] = None
            try:
                station["repacked_channel"] = (
                    re.search(r"Repacked Channel: \d*", str(st))
                    .group(0)
                    .replace("Repacked Channel: ", "")
                )
            except:
                station["repacked_channel"] = None
            try:
                station["repacking_dates"] = (
                    re.search(
                        r"Repacking Dates: \d*\/\d*\/\d* to \d*\/\d*\/\d*", str(st)
                    )
                    .group(0)
                    .replace("Repacking Dates: ", "")
                )
            except:
                station["repacking_dates"] = None
            try:
                station["rf_channel"] = (
                    re.search(r"RF Channel: .\d", str(st))
                    .group(0)
                    .replace("RF Channel: ", "")
                )
            except:
                station["rf_channel"] = None
            station["city_of_license"] = (
                re.search(
                    r"City of License: [a-z-A-Z .&/;`]*[,]*[A-Z]*[,][ A-Z]*",
                    str(st),
                )
                .group(0)
                .replace("City of License: ", "")
            )
            page_data.append(station)
            print(station)
browser.close()
