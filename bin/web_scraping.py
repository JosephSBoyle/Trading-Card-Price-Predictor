from selenium import webdriver
import re
import matplotlib.pyplot as plt
import numpy as np

#TODO Implement 403 handling e.g wait and retry @
#TODO Generate List of card URLS using MTGJSON @


class Visualiser:
    @staticmethod
    def plot_price(dates: list, prices: list):
        plt.figure(figsize=(6, 6))
        plt.xticks(rotation=90)
        plt.plot(dates, prices, lw=5)
        plt.ylabel("Price / £")
        plt.xlabel("Date")
        plt.show()


class Scraper:
    def __init__(self):
        self.extension_path = "C:\\Users\\Extasia\\Desktop\\python\\I-don&#39;t-care-about-cookies_v2.9.2.crx"
        self.webdriver_path = "C:\\Users\\Extasia\\Desktop\\python\\chromedriver.exe"

    def get_info(self, card_url: str) -> dict:
        """
        :param card_url: URL to scrape from e.g: https://www.cardmarket.com/en/Magic/Products/Singles/%SET%/%CARD%
        :return: dictionary containing basic info scraped from the URL: price, date, min_price, #available
        """
        parsed_response = {"price": [],
                           "date": [],
                           "available_items": int(),
                           "available_foils": int()}

        options = webdriver.ChromeOptions()
        options.add_extension(self.extension_path)
        options.add_argument("--headless")
        try:
            driver = webdriver.Chrome(self.webdriver_path, chrome_options=options)
            driver.minimize_window()
            driver.get(card_url)
        except Exception as e:
            print(e)

        # find the number of available items
        try:
            avail = driver.find_element_by_css_selector(
                "#tabContent-info > div > div.col-12.col-lg-6.mx-auto > div >"
                " div.info-list-container.col-12.col-md-8.col-lg-12.mx-auto.align-self-start > "
                "dl > dd:nth-child(10)").get_attribute('innerHTML')
            parsed_response["available_items"] = int(avail)
        # Sometimes the structure of the page varies
        except ValueError:
            try:
                avail = driver.find_element_by_css_selector(
                    "#tabContent-info > div > div.col-12.col-lg-6.mx-auto >"
                    " div > div.info-list-container.col-12.col-md-8.col-lg-12.mx-auto.align-self-start > "
                    "dl > dd:nth-child(8)").get_attribute('innerHTML')
                parsed_response["available_items"] = int(avail)
            except Exception as e:
                print(e)
        # find the two week price history
        try:
            items = driver.find_elements_by_class_name('chart-init-script')
            item = items[0]  # 0th element contains prev MONTH's data, 1st elem is past 2 weeks.
            txt = item.get_attribute("text")

            dates = [re.sub('[^0-9.]', '', date) for date in (txt[txt.find('['):txt.find(']')].split(','))]
            dates = dates[1:]

            d1 = 'Price","data":['      # start//end delimiters for scraping the info we need
            d2 = '],"backgroundColor"'

            prices = [re.sub('[^0-9.]', '', price) for price in (txt[txt.find(d1):txt.find(d2)].split(','))]
            prices = prices[2:]
            prices = list(map(float, prices))

            parsed_response["price"] = prices
            parsed_response["date"] = dates
            parsed_response["mean_price"] = np.mean(prices)

        except Exception as e:
            print(e)

        # find the number of available foils
        try:
            driver.find_element_by_css_selector(
                "#tabContent-info > div > div.col-12.text-right.small > label > span.switch").click()
            avail_foils = driver.find_element_by_css_selector(
                "#tabContent-info > div > div.col-12.col-lg-6.mx-auto > div >"
                " div.info-list-container.col-12.col-md-8.col-lg-12.mx-auto.align-self-start > "
                "dl > dd:nth-child(10)").get_attribute('innerHTML')
            parsed_response["available_foils"] = int(avail_foils)
        except ValueError:
            try:
                avail_foils = driver.find_element_by_css_selector(
                    "#tabContent-info > div > div.col-12.col-lg-6.mx-auto > div > "
                    "div.info-list-container.col-12.col-md-8.col-lg-12.mx-auto.align-self-start > dl > dd:nth-child(8)"
                ).get_attribute('innerHTML')
                parsed_response["available_foils"] = int(avail_foils)
            except Exception as e:
                print(e)

        driver.__exit__()
        return parsed_response


# s = Scraper()
# card_info = s.get_info(card_url="https://www.cardmarket.com/en/Magic/Products/Singles/Core-2020/Lotus-Field")
#
# if card_info != "Scraping Error":
#     Visualiser.plot_price(card_info["date"], card_info["price"])
#     print(card_info)
