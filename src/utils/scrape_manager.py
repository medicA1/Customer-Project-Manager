from selenium.webdriver.common.by import By
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from db.db_manager import DatabaseManager
import time

class ScrapeManager():
    def __init__(self, session):
        self.IKEA_BASE_URL = "https://www.ikea.com/hr/hr/"
        self.LESNINA_BASE_URL = "https://www.xxxlesnina.hr"
        self.IKEA_SEARCH_SIGN = "search/?q="
        self.LESNINA_SEARCH_SIGN = "/s/?s="
        self.session = session

        self.dm = DatabaseManager(self.session)

    def convert_price_to_float(self, price):
        """
        Converts a price string to a float value.
        This function handles price strings in formats commonly used,
        where the comma is used as the decimal separator and the period as the
        thousand separator. It also handles cases where the currency symbol '€'
        is present and where the dash '‒' indicates zero cents.
        """
        price_without_currency = price.replace("€", "").strip()
        price_normalized = price_without_currency.replace("‒", ".00")
        price_normalized = price_normalized.replace(",", ".")
        parts = price_normalized.split(".")
        if len(parts) > 2:
            price_normalized = "".join(parts[:-1]) + "." + parts[-1]
        try:
            return float(price_normalized)
        except ValueError as e:
            print(f"Error converting price to float: {e}")
            return None
    
    def url_template(self, base_url, article_number, search_sign):
        """
        Constructs a URL by concatenating a base URL, a search sign (query parameter or path segment), and an article number.
        This function is designed to generate URLs for article lookup based on a consistent URL structure.
        """
        article_url = base_url + search_sign + article_number
        return article_url
    
    def get_browser(self, browser):
        # Use browser_combobox.get() for browser
        if browser == "Mozilla Firefox":
            return webdriver.Firefox()
        if browser == "Google Chrome":
            return webdriver.Chrome
        raise ValueError(f"Unsupported browser: {browser}")
    
    def wait_condition(self, driver, locator):
        products_locator = (By.CSS_SELECTOR, locator)
        products = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located(products_locator)
        )

    def wait_for_element_by_id(self, driver, element_id):
        element_locator = (By.ID, element_id)
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(element_locator)
        )

    def generate_article_url(self, manufacturer, article_number):
        if manufacturer == "Ikea":
            return self.url_template(self.IKEA_BASE_URL, article_number, self.IKEA_SEARCH_SIGN)
        elif manufacturer == "Lesnina":
            return self.url_template(self.LESNINA_BASE_URL, article_number, self.LESNINA_SEARCH_SIGN)
        else:
            raise ValueError(f"Unsupported manufacturer: {manufacturer}")
        
    def scrape_ikea(self, project_id, url, driver, amount):
            """
            Scrapes IKEA product information from a given URL and stores it in the database.
            This function navigates to a specified IKEA product listing page using Selenium, waits for the product list to load, and then extracts product details using BeautifulSoup.
            """
            driver.get(url)
            locator = ".plp-mastercard  "
            self.wait_condition(driver, locator)
            html = driver.page_source
            page = BeautifulSoup(html, "html.parser")

            product_families = page.select(".notranslate.plp-price-module__product-name")
            product_descriptions = page.select(".plp-price-module__description")
            art_numbers = page.select(".search-summary__content h1 b")
            urls = page.select('.plp-mastercard__item.plp-mastercard__image a')
            prices = page.select(".plp-price__sr-text")

            for product_family, product_description, art_number, amount, price, url in zip(product_families, product_descriptions, art_numbers, amount, prices, urls):
                price_float = self.convert_price_to_float(price.text)
                self.dm.add_furniture_data(product_family.text, product_description.text, art_number.text, amount, price_float, url["href"], project_id)
    
    def scrape_lesnina(self, project_id, url, driver, amount):
        driver.get(url)
        time.sleep(4)
        html = driver.page_source
        page = BeautifulSoup(html, "html.parser")

        product_family = page.find('a',  href=re.compile(r'^/c/brend-')).find('span')
        product_family_element = product_family.text
        product_descriptions = page.find_all(attrs={"data-purpose": "productName.heading-2-h1"})
        product_measurements = page.find_all(attrs={"data-purpose": "product.productAttributes"})
        art_numbers = page.find_all(attrs={"data-purpose": "product.productNumber"})
        prices = page.find_all(attrs={"data-purpose": "product.price.current"})

        for product_description, product_measurement, art_number, price in zip(product_descriptions, product_measurements, art_numbers, prices):
            full_description = product_description.text + product_measurement.text
            price_float = self.convert_price_to_float(price.text)
            art_number = art_number.text[-10:]
            self.dm.add_furniture_data(product_family_element, full_description, art_number, amount, price_float, url, project_id)

        