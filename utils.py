import numpy as np


def safe_to_excel(df, filename):
    """
    :param df: pandas DataFrame
    :param filename: path in which to save the XLSX file.
    "Safe save" an XL file.
    """
    while True:
        try:
            df.to_excel(filename)
            break
        except PermissionError:
            print("Cannot write to an open Excel file.")
            pass


def classify(current, future, threshold=0) -> bool:
    """
    :param current: current price
    :param future: price n days after "current"
    :param threshold: the threshold price change above which a sample is considered a "buy"
    :return: boolean 1: "buy", 2: "sell"
    """
    if float(future) > float(current + threshold):
        return bool(1)
    else:
        return bool(0)


def normalize(x: np.array):
    """
    :param x: array of floats
    :return: x: normalized array
    """

    arr_mean = np.nanmean(x)
    inds = np.where(np.isnan(x))
    x[inds] = arr_mean
    x = (x - min(x)) / (max(x) - min(x))
    return x
