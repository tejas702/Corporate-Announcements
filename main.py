import asyncio
import os
import urllib.request
import requests

from PyPDF2 import PdfReader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Chrome/51.0.2704.103",
}


async def download_pdf(url, filename, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        print(response.status_code)


options = ChromeOptions()
options.headless = True

url = "https://www.bseindia.com/corporates/ann.html"

driver = webdriver.Chrome(options=options)

driver.get(url)


elements = driver.find_elements(
    By.CLASS_NAME, 'tablebluelink')


skip = True

i = 1

data = []

keywords = ["Target entity", "Amalgamation",
            "Preferential allotment", 'Rights issue', 'Capacity expansion']

####################################################

for ele in elements:
    if (skip):
        skip = False
        continue

    xpath = '//*[@id = "lblann"]/table/tbody/tr[4]/td/table[' + \
        str(i) + ']/tbody/tr[1]/td[1]/a'

    title = driver.find_element(
        By.XPATH, xpath).text

    link = ele.get_attribute('href')

    filename = 'file.pdf'

    asyncio.run(download_pdf(link, filename, headers))

    reader = PdfReader('file.pdf', strict=False)
    number_of_pages = len(reader.pages)

    txt = ""
    for page in reader.pages:
        txt += page.extract_text().lower()

    txt = txt.split(' ')

    keys = []
    for key in keywords:
        if (key.lower() in txt):
            keys.append(key)

    data.append({'title': title, 'link': link, 'keywords': keys})

    i += 1

##############################################################

os.remove('file.pdf')

driver.quit()

print(data)
