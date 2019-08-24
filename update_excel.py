"""
RUN this file to update the excel spreadsheet containing the price history of all the cards contained in the JSON files
in the /data folder.
"""
from bin.generate_urls import JsonParser
from bin.web_scraping import Scraper
from bin.utils import safe_to_excel
import pandas as pd
import numpy as np
import time
from tqdm import tqdm  # creates a loading bar to track the scraping of the url_list

scraped_data = []

j = JsonParser()
url_list = j.generate_urls()  # read JSON files from /data
start = time.time()
num = len(url_list)

for i, url in enumerate(tqdm(url_list)):
    print(f"url {i} of {num} urls")
    s = Scraper()
    card_info = s.get_info(card_url=url)
    scraped_data.append(card_info)

end = time.time()
print(end-start)

XL = pd.DataFrame(pd.read_excel(r"C:\Users\Extasia\PycharmProjects\MTG predictor\data\dataframe.xlsx"))
print(len(scraped_data))
print(len(XL.index))

arr = list(np.zeros(len(XL.index)-len(scraped_data)))

XL["prices"] = scraped_data + arr
safe_to_excel(XL, r"C:\Users\Extasia\PycharmProjects\MTG predictor\data\dataframe.xlsx")
