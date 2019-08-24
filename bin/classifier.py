def classify(current, future, threshold=0.5):
    if future > float(current+threshold):
        return 1  # Buy
    else:
        return 0  # Sell
