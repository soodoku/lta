from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re

# used driver on this link https://chromedriver.storage.googleapis.com/94.0.4606.41/chromedriver_linux64.zip
browser = webdriver.Chrome("./chromedriver")
browser.get("https://www.fcc.gov/media/engineering/dtvmaps")
input_box = browser.find_element(By.ID, "startpoint")
input_box.send_keys("00501")
time.sleep(2)
browser.find_element(By.ID, "btnSub").click()
time.sleep(5)
# scrape data
# frist get table having data
soup = BeautifulSoup(browser.page_source, "html.parser")
table_soup = soup.find("div", {"id": "contourdata"})
tables = table_soup.find_all("table")
data_table = tables[2]
# get rows
data_table = data_table.find("tbody")
data = {}
for strength in [1, 2, 3, 4]:
    for row in data_table.find_all("tr", {"class": f"strength{strength}"}):
        st = re.findall(r'onclick="getdetail(.*)" style="', str(row))
        Facility_ID = re.findall(r"Facility ID:\d*", str(st))
        station = {
            "zipcode": "temp",
            "callsign": row.find_all("td")[1].text.replace("\n", ""),
            "network": row.find_all("td")[2].text.replace("\n", "").replace(" ", ""),
            "channel_number": row.find_all("td")[3]
            .text.replace("\n", "")
            .replace(" ", ""),
            "band": row.find_all("td")[4].text.replace("\n", "").replace(" ", ""),
            "signal_strength": strength,
            "facility_id": re.search(r"Facility ID: \d*", str(st))
            .group(0)
            .replace("Facility ID: ", ""),
            "city_of_license": re.search(r"City of License.*, ", str(st))
            .group(0)
            .replace("City of License: ", "")[:-2],
            "rx_strength": re.search(r"RX Strength: .\d", str(st))
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
                re.search(r"Repacking Dates: \d*", str(st))
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
        data["temp"] = station
