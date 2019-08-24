from bin.generate_urls import JsonParser
from bin.web_scraping import Scraper
from bin.utils import safe_to_excel
import time
import pandas as pd
import numpy as np
from tqdm import tqdm

j = JsonParser()

scraped_data = []
url_list = j.generate_urls()  # also creates XL file with this info
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
