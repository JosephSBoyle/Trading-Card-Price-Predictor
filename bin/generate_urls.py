import json
import pandas as pd
import os
from os import path
from bin.utils import safe_to_excel


class JsonParser:
    def __init__(self):
        self.data_folder = r"C:\Users\Extasia\PycharmProjects\MTG predictor\data"
        self.excel_filename = f"{self.data_folder}\dataframe.xlsx"

    @staticmethod
    def read_json(fp) -> list:
        """
        :param fp: json filepath
        :return: list of lists -> [name, rarity, CMC, mkm URL]
        """
        with open(fp, "rb") as js:
            json_ = dict(json.load(js))
            cards = json_["cards"]
            relevant_cards = []
            keys = ["name", "rarity", "convertedManaCost"]

            for card in cards:
                purchase_urls = card["purchaseUrls"]  # URL's for purchasing selected card
                try:
                    url = dict(purchase_urls)['cardmarket']
                    if card["rarity"] in ("mythic", "rare", "uncommon"):
                        row = [card.get(key) for key in keys]
                        row.append(url)
                        relevant_cards.append(row)

                # Some cards e.g those contained in entry decks do not have mkm urls
                except KeyError:
                    print(f"No URL exists for: {card['name']}")
                    pass
        return relevant_cards

    def generate_urls(self) -> list:
        """
        Open all JSON's in the data folder and collect them in an EXCEL file, then remove duplicate entries.
        :return: list: mkm urls
        """
        for file in os.listdir(self.data_folder):
            if file.split(".")[-1] == "json":
                df = pd.DataFrame(
                    JsonParser.read_json(r"C:\Users\Extasia\PycharmProjects\MTG predictor\data\{}".format(file)),
                    columns=("name", "rarity", "CMC", "mkm URL"))
                if path.exists(self.excel_filename):
                    existing_df = pd.read_excel(self.excel_filename)
                    df = pd.DataFrame(pd.concat([existing_df, df], ignore_index=True))

                # remove duplicate card entries.
                df = df.drop_duplicates(keep="first")
                safe_to_excel(df, self.excel_filename)
        return list(df["mkm URL"])


