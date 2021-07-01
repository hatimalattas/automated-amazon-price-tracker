from bs4 import BeautifulSoup
import requests
import smtplib
import os

PRODUCT_NAME = "Google Nest"
TARGET_PRICE = 450

amazon_product_url = "https://www.amazon.com/Google-Nest-WiFi-Router-Generation/dp/B08F1YPMS1?th=1"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Accept-Language": "en-US,en;q=0.5",
}

response = requests.get(url=amazon_product_url, headers=headers)

amazon_product_web_page = response.text

soup = BeautifulSoup(amazon_product_web_page, 'html.parser')

product_name = soup.select_one("#productTitle").get_text().strip()

scraped_price = soup.select_one("#priceblock_ourprice").string
price = float(scraped_price.split("$")[1])


# Sender Email information
my_email = os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")

if price < TARGET_PRICE:
    msg = f"{PRODUCT_NAME} is now ${price}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="alattas96@outlook.com",
            msg=f"Subject:Amazon Price Alert!\n\n{msg}"
        )
