import csv
import time
import requests
from bs4 import BeautifulSoup
csv_file = 'Amazon Scraping - Sheet1.csv'


def csv_extractor(file_name):
    countrys = []
    asins = []
    urls = []
    with open(file_name, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            countrys.append(row['country'])
            asins.append(row['Asin'])
    for i in range(len(countrys)):
        urls.append(f"https://www.amazon.{countrys[i]}/dp/{asins[i]}")
    return urls


def import_files_from_url_list():
    list_name = csv_extractor(csv_file)
    all_details_from_urls_to_list = []
    count = 0
    sample = (100, 200, 300, 400, 500, 600, 700, 800, 900, 1000)
    start_time = time.time()
    for i in list_name:
        count += 1
        response = requests.get(i)
        soup = BeautifulSoup(response.content, "html.parser")
        if response.status_code == 200:
            title = soup.find(id="productTitle").get_text()
            price = soup.find(class_="a-offscreen").text
            product_details = soup.find(id="feature-bullets").text
            img_url = soup.find(id="imgTagWrapperId")
            all_details = dict(title=title, img_url=img_url, price=price, product_details=product_details,
                               message=f"{i} with the status code {response.status_code}")
            all_details_from_urls_to_list.append(all_details)
        else:
            all_details = dict(error=f"{i} is not available with the status code {response.status_code}")
            all_details_from_urls_to_list.append(all_details)
        if count == 1000:
            end_time_of_100_datas = time.time()
            time_taken = end_time_of_100_datas - start_time
            print(f"{time_taken} after completing with 1000 datas.")
            break
        if count in sample:
            end_time_of_100_datas = time.time()
            time_taken = end_time_of_100_datas - start_time
            print(f"{time_taken} seconds after completing {count} datas.")
            continue
    print("The details from the urls are ----\n", all_details_from_urls_to_list)


import_files_from_url_list()
