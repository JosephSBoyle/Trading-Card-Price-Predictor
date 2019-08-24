# TODO Append classifier.classify results as target variables based on mean week's prices - Done
"""
File containing all functions required in order to generate the input features pertaining to our ML model.
"""
from .utils import classify, normalize
import pandas as pd
import numpy as np
import ast


class Features:

    def __init__(self):
        #  days into the future we wish to predict
        self.FUTURE_DAYS_PREDICT = 7
        # simulating overhead costs, targets are cards which rise more than the threshold over the period
        self.THRESHOLD = 0.5
        # path to scraped data XL sheet
        self.XL_FILEPATH = r"C:\Users\Extasia\PycharmProjects\MTG predictor\data\dataframe.xlsx"

    def excel_to_dict(self) -> dict or None:
        df = pd.read_excel(self.XL_FILEPATH)
        assert type(df) == pd.DataFrame
        card_dict = {}
        if "prices" not in df.columns:
            print("No price info in the XL file. Run the webscraper prior to this function.")
            return
        for i in df.index:
            try:
                name = df.iloc[i]["name"]
                info = df.iloc[i]["prices"]
                try:
                    card_dict[name] = ast.literal_eval(info)

                # e.g the scraper was unable to get the info
                except ValueError:
                    card_dict[name] = None
            except IndexError:
                pass
        return card_dict

    @staticmethod
    def dict_to_df(card_dict: dict) -> pd.DataFrame:
        main_df = pd.DataFrame()  # begin empty

        for card in card_dict.keys():
            df = pd.DataFrame(card_dict[card], columns=["date", "price"])
            df.columns = ["date", f"{card}_price"]
            if len(main_df) == 0:  # if the df is empty
                main_df = df  # then it's just the current df
            else:
                # otherwise, join this data to the main one
                # https://stackoverflow.com/questions/53645882/pandas-merging-101 MERGE GOD!!!
                main_df = main_df.merge(df, on='date', how='outer')

        # Dayfirst is the format of our data as opposed to the US format to which the data is converted for comp. w/ pd
        main_df["date"] = pd.to_datetime(main_df['date'], dayfirst=True)
        main_df.set_index("date")
        main_df = main_df.sort_values("date")
        return main_df

    def insert_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        for x, col in enumerate(df.columns):
            if col == "date":
                pass
            else:
                try:
                    t_col = f"{col}".replace("price", "target")  # "target" col name
                    f_col = f"{col}".replace("price", "future")  # "future" col name

                    df.insert(column=t_col, value=0, loc=(3 * x - 1))
                    df.insert(column=f_col, value=0, loc=(3 * x - 1))

                    # future col is the price n days into the future from the current column
                    df[f_col] = df[col].shift(-self.FUTURE_DAYS_PREDICT)

                    # target col is whether or not this cur / fut pricing corresponds to a "Buy" or a "Sell"
                    df[t_col] = list(map(classify, df[col], df[f_col]))
                except ValueError:
                    pass
        return df

    @staticmethod
    def preprocess_df(df):
        for col in df.columns:
            if "_future" in str(col):
                df = df.drop(col, 1)  # don't need this anymore.

        for col in df.columns[1:]:  # go through all of the columns
            if "_target" not in str(col):  # normalize all ... except for the target itself!
                df[col] = (normalize(np.array(df[col])))
        return df

    # TODO Normalise the columns without the NaN values

    # TODO Investigate "low pass filtering" (smoothing?)
