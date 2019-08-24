import numpy as np


def safe_to_excel(df, filename):
    """
    :param df: pandas DataFrame
    :param filename: path in which to save the XLSX file.
    :return:
    """
    while True:
        try:
            df.to_excel(filename)
            break
        except PermissionError:
            print("Cannot write to an open Excel file.")
            pass


def classify(self, current, future) -> bool:
    if float(future) > float(current + self.THRESHOLD):
        return bool(1)
    else:
        return bool(0)


def normalize(x: np.array):
    arr_mean = np.nanmean(x)
    inds = np.where(np.isnan(x))
    x[inds] = arr_mean
    x = (x - min(x)) / (max(x) - min(x))
    return x
