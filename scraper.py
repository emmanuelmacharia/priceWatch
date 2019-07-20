import smtplib
import time
import os

import requests
from bs4 import BeautifulSoup

URL = "https://www.amazon.com/OnePlus-Factory-Unlocked-Verizon-Tmobile/dp/B07RR455Z3/ref=sr_1_3?_encoding=UTF8&keywords=Oneplus%2B7%2Bpro&path=%2Fs%3Fk%3DOneplus%2B7%2Bpro&qid=1563556544&s=wireless&sr=1-3&useRedirectOnSuccess=1&th=1"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3843.0 Safari/537.36 Edg/77.0.218.4"}

def check_price():
    page = requests.get(URL, headers = headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text()

    price = soup.find(id= "priceblock_ourprice")

    converted_price = float(price[0:5])

    if converted_price < 750:
        send_mail()

    print(title)


def send_mail():
    '''sends emails to google'''
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    email = os.getenv('EMAIL_FROM')
    email_to = os.getenv('EMAIL_TO')
    email_password = os.getenv('EMAIL_PASSWORD')

    server.login(email, email_password)
    subject = "The price fell"
    body = "Check this out! " + URL

    msg = f"Subject: {subject} \n\n{body}"

    server.sendmail(
        email,
        email_to,
        msg
    )

    server.quit()

while(True):
    check_price()
    time.sleep((60*60*24*30))

