from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

url = 'https://www.bukalapak.com/c/fashion-wanita/jilbab-2571?from=omnisearch&from_keyword_history=false&search%5Bkeywords%5D=jilbab&search%5Bsort_by%5D=weekly_sales_ratio%3Adesc&search%5Btodays_deal%5D=0&search_source=omnisearch_keyword&source=navbar'

# options = Options()
# options.add_argument("--headless")
browser = webdriver.Chrome("chromedriver.exe")
browser.get(url)
html = browser.page_source
soup = BeautifulSoup(html, 'lxml')


data = []
table = soup.find_all('div', {"class": "bl-product-card"})
for x, div in enumerate(table):
    name = div.find("div", class_="bl-product-card__description-name").text
    harga = div.find("p", class_="bl-text--semi-bold").text
    lokasi = div.find("span", class_="bl-product-card__location").text
    rating = div.find("p", class_="bl-text--subdued").text

    terjual = div.find("div", class_="bl-product-card__separator")
    next_terjual = terjual.find_next_sibling(
        "p", class_="bl-text--subdued").text

    fix_name = name.replace('\n', ' ').replace('\r', '')
    fix_harga = harga.replace('\n', ' ').replace('\r', '')
    fix_rating = rating.replace('\n', ' ').replace('\r', '')
    fix_terjual = next_terjual.replace('\n', ' ').replace('\r', '')
    fix_lokasi = lokasi.replace('\n', ' ').replace('\r', '')

    obj = {
        "name": fix_name.strip(),
        "price": fix_harga.strip(),
        "rating": fix_rating.strip(),
        "location": fix_lokasi.strip(),
        "sold": fix_terjual.strip(),
    }
    data.append(obj)

print(data)
