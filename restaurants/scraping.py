from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
from pathlib import Path
from datetime import datetime
from pytz import timezone
import pandas as pd
import sys

# main_link = 'https://www.tripadvisor.com/Restaurants-g298507-St_Petersburg_Northwestern_District.html'


class RestaurantParser(object):

    def __init__(self, main_link):

        service = Service(str(Path.cwd().joinpath('chromedriver.exe')))
        options = ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--window-size=%s" % "1920,1080")
        self.browser = Chrome(service=service, options=options)
        self.browser.command_executor.set_timeout(5)
        self.browser.get(main_link)

    def start_parsing(self, pages_to_scrap):

        pages_count = 0
        button_path = '//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a'
        scraped_pages = [x for x in Path.cwd().joinpath('restaurants', 'pages').iterdir()]
        if scraped_pages:
            pages_count = max([(int(x.name.split('.')[0].split('_')[1])) for x in scraped_pages])
            print(datetime.now().astimezone(timezone("Europe/Moscow")).strftime("%d-%m-%Y %H:%M:%S"),
                  f'Moving to page {pages_count}...')
            for i in range(pages_count):
                next_page = self.browser.find_element(By.XPATH, button_path)
                next_page.click()
                sleep(2)
                button_path = '//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a[2]'

        pages_scrapped = 0
        while not pages_scrapped + pages_count == pages_to_scrap + pages_count:
            try:
                print(datetime.now().astimezone(timezone("Europe/Moscow")).strftime("%d-%m-%Y %H:%M:%S"),
                      f'Page {pages_scrapped + pages_count}')
                main_soup = BeautifulSoup(self.browser.page_source, 'lxml')
                self.parse_restaurant_page(main_soup, pages_scrapped + pages_count)
                sleep(2.5)
            except:
                print(datetime.now().astimezone(timezone("Europe/Moscow")).strftime("%d-%m-%Y %H:%M:%S"),
                      f'Error on page {pages_scrapped + pages_count}. Moving to next page...')
            pages_scrapped += 1
            next_page = self.browser.find_element(By.XPATH, button_path)
            next_page.click()
            button_path = '//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a[2]'

    def parse_restaurant_page(self, restaurant_list_soup, page):

        dataframe_dictionary = {'Latitude': [], 'Longitude': [], 'Name': [], 'Address': [],
                                # 'E-mail': [], 'Phone': [],
                                'Rating': [], 'Price category': [], 'Price range': [], 'Website': [],
                                'Cuisines': [], 'Special diets': []}

        for link in restaurant_list_soup.find_all('div', 'OhCyu'):
            full_link = f"https://www.tripadvisor.com{link.a['href']}"
            self.browser.execute_script('window.open("{}","_blank");'.format(full_link))
            self.browser.switch_to.window(self.browser.window_handles[-1])
            restaurant_soup = BeautifulSoup(self.browser.page_source, 'lxml')
            try:
                restaurant_info = self.get_restaurant_info(restaurant_soup)
                for key, value in restaurant_info.items():
                    dataframe_dictionary[key].append(value)
            except:
                pass
            self.browser.close()
            self.browser.switch_to.window(self.browser.window_handles[0])
            sleep(2)
        pd.DataFrame(dataframe_dictionary).to_excel(Path.cwd().joinpath('restaurants', 'pages',
                                                                        f'page_{page}.xlsx'))

    @staticmethod
    def get_restaurant_info(current_page):
        name = current_page.h1.text.split(',')[0]
        address = current_page.find('div', 'cSPba bKBJS Me').text
        rating = current_page.find('div', 'eEwDq').span.text.strip() if current_page.find('div', 'eEwDq') else 'no_data'
        try:
            latitude, longitude = current_page.find('div', 'cSPba bKBJS Me').a['href'].split('@')[1].split(',')
        except:
            latitude, longitude = 'no_data', 'no_data'
        try:
            website = current_page.find('div', 'bKBJS Me enBrh').a['href']
        except:
            website = 'no_data'
        #     email = current_page.find_all('div', 'bKBJS Me enBrh')[1].a['href']
        #     start, end = email.find(':') + 1, email.find('?')
        #     email = email[start:end]
        #     phone = current_page.find('div', 'bKBJS Me').text
        price_category = len(current_page.find('a', 'drUyy').text.split(' - ')[0]) \
            if current_page.find('a', 'drUyy') else 'no_data'
        price_range = current_page.find(text='PRICE RANGE').parent.parent.text.replace('PRICE RANGE', '').replace(
            '\xa0', '') if current_page.find(text='PRICE RANGE') else 'no_data'
        special_diets = current_page.find(text='Special Diets').parent.parent.text.replace(
            'Special Diets', '') if current_page.find(text='Special Diets') else 'no_data'
        cuisines = current_page.find(text='CUISINES').parent.parent.text.replace('CUISINES', '') if current_page.find(
            text='CUISINES') else 'no_data'

        return {'Latitude': latitude, 'Longitude': longitude, 'Name': name, 'Address': address,
                #             'E-mail': email, 'Phone': phone,
                'Rating': rating, 'Price category': price_category, 'Price range': price_range,
                'Website': website, 'Cuisines': cuisines, 'Special diets': special_diets}


if __name__ == '__main__':
    parser_object = RestaurantParser(sys.argv[1])
    parser_object.start_parsing(int(sys.argv[2]))

