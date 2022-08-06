import os
import requests
import json
from flask import Flask, jsonify
import datetime
from flask_cors import CORS

from PyPDF2 import PdfReader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions

headers = {
    "User-Agent": "Chrome/51.0.2704.103",
}


def download_pdf(url, filename, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        print(response.status_code)


options = ChromeOptions()
options.headless = True

url = "https://www.bseindia.com/corporates/ann.html"

driver = webdriver.Chrome(executable_path="F:/Corporate-Announcements/chromedriver.exe", options=options)

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
    if skip:
        skip = False
        continue

    xpath = '//*[@id = "lblann"]/table/tbody/tr[4]/td/table[' + \
            str(i) + ']/tbody/tr[1]/td[1]/a'

    title = driver.find_element(
        By.XPATH, xpath).text

    link = ele.get_attribute('href')

    filename = 'file.pdf'

    download_pdf(link, filename, headers)

    try:
        reader = PdfReader('file.pdf', strict=False)
        txt = ""
        for page in reader.pages:
            txt += page.extract_text().lower()
        txt = txt.split(' ')
        keys = []
        for key in keywords:
            if key.lower() in txt:
                keys.append(key)
        print("pdf read")
    except:
        print("cant read pdf")

    data.append({'title': title, 'link': link, 'keywords': keys})

    i += 1

##############################################################
try:
    os.remove('file.pdf')
except:
    print("No pdf file found")

driver.quit()

json_object = json.dumps(data, indent=4)

#print(json_object)

# Initialize Flask:

x = datetime.datetime.now()

# Initializing flask app
app = Flask(__name__)
CORS(app)

# Route for seeing a data
@app.route('/')
def get_time():
    # Returning an api for showing in  reactjs
    return jsonify(data)


# Running app
if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
