from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
import pymongo
import re
import json

url = 'https://shopee.co.id/search?keyword=bahan%20kain&page=0'

# options = Options()
# options.add_argument("--headless")
browser = webdriver.Chrome("chromedriver.exe")
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["admin"]
collection = db["marketplace"]

batch_number = "Batch-" + datetime.today().strftime('%Y%m%d') + "-" + \
    str(random.randint(1, 999999999999))


def search(base_url):
    browser.get(base_url)
    time.sleep(5)
    browser.execute_script('window.scrollTo(0, 1500);')
    time.sleep(5)
    browser.execute_script('window.scrollTo(0, 2500);')
    time.sleep(5)
    html = browser.page_source
    # browser.close()
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all(
        'div', {"class": "bl-product-card__description-name"})
    data = []
    for x, div in enumerate(table):
        tag_link = div.find("a")
        if tag_link is not None:
            data.append(tag_link.get('href'))

    return data


def getProductName(soup):
    div_product_name = soup.find("h1", class_="c-main-product__title")
    if div_product_name is not None:
        return div_product_name.text

    # label_product_name = soup.find("span", class_ = "OSgLcw")
    # if label_product_name is not None:
    # 	product_name = label_product_name.text
    # 	return product_name

    # div_title = soup.find("span", class_ = "$0")
    # if div_title is not None:
    # 	product_name = div_title.text
    # 	return product_name

    return ''


def getMerek(soup):
    label_merek = soup.find("th", string="Brand")
    if label_merek is not None:
        merek = label_merek.find_next_sibling("td")
        merek2 = merek.find_next_sibling("td")
        return merek2.text

    return ''


def getBahan(soup):
    label_bahan = soup.find("th", string="Bahan")
    if label_bahan is not None:
        bahan = label_bahan.find_next_sibling("td")
        bahan2 = bahan.find_next_sibling("td")
        return bahan2.text

    return ''


def getStyle(soup):
    label_bahan = soup.find("th", string="Type")
    if label_bahan is not None:
        bahan = label_bahan.find_next_sibling("td")
        bahan2 = bahan.find_next_sibling("td")
        return bahan2.text

    return ''


def getProductOrigin(soup):
    label_bahan = soup.find("th", string="Asal")
    if label_bahan is not None:
        bahan = label_bahan.find_next_sibling("td")
        bahan2 = bahan.find_next_sibling("td")
        return bahan2.text

    return ''


def removeHiddenSpace(teks):
    name = teks.replace('\n', ' ').replace('\r', '')
    return name.strip()


def product_detail(url_suffix):
    # url_detail = url_suffix
    browser.get(url_suffix)
    time.sleep(5)
    browser.execute_script('window.scrollTo(0, 1500);')
    time.sleep(5)
    browser.execute_script('window.scrollTo(0, 2500);')
    time.sleep(5)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    data = []

    # PRODUCT NAME
    product_name = getProductName(soup)
    shop_name = soup.find("h3", class_="c-seller__name").text

    string_price = soup.find(
        'div', {'class': 'c-product-price'}).find('span').text
    remove_dot = string_price.replace(".", "")
    price = remove_dot.replace("Rp", "")

    span_rating = soup.find("span", class_="summary__score")
    rating = ''
    if span_rating is not None:
        rating = span_rating.text

    merek = getMerek(soup)
    bahan = getBahan(soup)
    style = getStyle(soup)
    dimensi = ''

    label_location = soup.find(
        "div", class_="c-main-product__location__name").text
    location = removeHiddenSpace(label_location)

    product_origin = getProductOrigin(soup)

    label_stock = soup.find("div", class_="u-txt--base").text
    stock = int(re.search(r'\d+', label_stock).group())

    is_insert = False
    include_category = ["Grosir Fashion Wanita",
                        "Fashion Wanita", "Busana Muslim"]
    product_category = []
    for temp_category in soup.find_all("a", class_="c-bl-breadcrumb__item-text"):
        if temp_category.text in include_category:
            is_insert = True
        product_category.append(temp_category.text)

    if not is_insert:
        return False

    description = soup.find(
        "div", class_="c-information__description-txt").text
    div_sold = soup.find("div", class_="c-main-product__rating")
    sold = ''
    if div_sold is not None:
        string_sold = div_sold.find_next_sibling("span").text
        sold = int(re.search(r'\d+', string_sold).group())

    string_review = soup.find("div", class_="c-main-product__rating")
    total_review = ''
    if string_review is not None:
        total_review = int(re.search(r'\d+', string_review.text).group())

    div_shop_category = soup.find(
        'div', {'class': 'c-main-product__wholesale-label'})
    shop_category = ''
    if div_shop_category is not None:
        shop_category = div_shop_category.text

    customer_review = []
    for temp_review in soup.find_all("div", class_="c-reviews-item"):
        customer_review.append(temp_review.text)

    product_color = []
    for temp_color in soup.find_all("span", class_="multiselect__option"):
        product_color.append(temp_color.text)

    obj = {
        'marketplace_name': 'bukalapak',
        'link': url_suffix,
        'shop_name': shop_name,
        'shop_category': shop_category,
        'location': location,
        'product_name': product_name,
        'product_category': product_category,
        'price': price,
        'rating': rating,
        'total_review':  total_review,
        'sold': sold,
        'merek': merek,
        'bahan': bahan,
        'dimensi': dimensi,
        'style': style,
        'product_origin': product_origin,
        'stock': stock,
        'product_color': product_color,
        'customer_review': customer_review,
        'description': description,
        'total_views': '',
        'insert_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'batch_number': batch_number
    }
    with open("D:\download\scrapping\data_marketplace_bukalapak_detail.json", "a") as data:
        data.write(json.dumps(obj) + ', ')
        data.close()
    return obj


all_data = []
limit = 1
for i in range(4):
    page = i + 1
    base_url = 'https://www.bukalapak.com/products?page=' + \
        str(page) + '&search%5Bkeywords%5D=bahan%20kain'
    product_urls = search(base_url)
    for index, product_url in enumerate(product_urls):
        temp = product_detail(product_url)
        if temp:
            all_data.append(temp)

        if index == limit:
            break

print(all_data)
# if all_data:
# 	x = collection.insert_many(all_data)
