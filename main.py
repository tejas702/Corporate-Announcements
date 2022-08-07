import os
import requests
import json
from flask import Flask, jsonify
import datetime
from flask_cors import CORS
import csv
import smtplib
import ssl

from PyPDF2 import PdfReader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions

# selenium setup
headers = {
    "User-Agent": "Chrome/51.0.2704.103",
}

options = ChromeOptions()
options.headless = True

url = "https://www.bseindia.com/corporates/ann.html"

driver = webdriver.Chrome(options=options)

driver.get(url)


# Initializing flask app
app = Flask(__name__)
CORS(app)


data = []
x = datetime.datetime.now()


def download_pdf(url, filename, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        print(response.status_code)


def scrape_data():
    i = 1
    skip = True
    elements = driver.find_elements(
        By.CLASS_NAME, 'tablebluelink')

    keywords = ["Target entity", "Amalgamation",
                "Preferential allotment", 'Rights issue', 'Capacity expansion']

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

            data.append({'title': title, 'link': link, 'keywords': keys})
            print("pdf read")
        except:
            print("cant read pdf")

        i += 1

    try:
        os.remove('file.pdf')
    except:
        print("No pdf file found")


def send_mail():
    message = """Subject: Your grade

    Hi {name}, your grade is {grade}"""
    from_address = "email"  # email
    password = "password"  # password

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(from_address, password)
        with open("contacts_file.csv") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for name, email, grade in reader:
                server.sendmail(
                    from_address,
                    email,
                    message.format(name=name, grade=grade),
                )


# Route for seeing a data
@app.route('/')
def get_data():
    print('flask started....')
    return jsonify(json.dumps(data, indent=4))


# main method
if __name__ == '__main__':
    scrape_data()
    # send_mail() # commented temporarily
    app.run(host="localhost", port=5000)
