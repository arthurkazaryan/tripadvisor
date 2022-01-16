# <div align="center">Tripadvisor Data Scraping and Analyzing</div>
<a href="https://www.tripadvisor.com/" title="Tripadvisor">Tripadvisor</a> is a web page to search for restaurants, hotels, apartments, etc. Current repo is made to store code for scraping data from Tripadvisor and currently is available only to scrape data about restaurants.

To scrape data Selenium and BeautifulSoup libraries are used. Make sure you have installed all libaries needed:

    pip install -r requirements.txt

In current script Selenium requires ``chromedriver.exe`` to operate. <a href="https://chromedriver.chromium.org/downloads" title="chromedriver">Download</a> and place it in the root of this repository.

## Restaurants
The script allows to scrape info about restaurants by passing URL and number of pages to scrape. Each page is being saved into ``./restaurants/pages`` folder. No personal data such as e-mails and phone numbers are being collected by default. To enable scraping such data, modify script by uncommenting all commented rows.

Type the following to run the script:

    python ./restaurants/scraping.py https://www.tripadvisor.com/Restaurants-g298507-St_Petersburg_Northwestern_District.html 100

The script was tested by scraping restaurants data in St. Petersburg. To see the analyze, <a href="https://github.com/arthurkazaryan/tripadvisor/blob/main/restaurants/README.md" title="readme">click here.</a>.
