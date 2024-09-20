#Flask Implementation
from flask import Flask, render_template, request, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from email.mime.text import MIMEText
import smtplib
import os

app = Flask(__name__)

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run headless (no GUI)
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
chrome_options.add_argument("--log-level=3")  # Suppress ChromeDriver logs
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

@app.route("/", methods=["GET", "POST"])
def track_price():
    if request.method == "POST":
        url = request.form["url"]
        price_wanted = float(request.form["price_wanted"])
        user_email = request.form["user_email"]
        
        # Scrape the price and title
        actual_price, prod_title = scrape_amazon_price(url)
        
        if actual_price is not None:
            send_confirmation_email(user_email, prod_title, price_wanted)
            if actual_price <= price_wanted:
                send_notification(url, price_wanted, user_email, actual_price, prod_title)
            
            return render_template("result.html", actual_price=actual_price, prod_title=prod_title, email_sent=actual_price <= price_wanted)
        else:
            return render_template("result.html", actual_price=None, prod_title=None, email_sent=False)

    return render_template("index.html")

def scrape_amazon_price(url):
    price, title = None, None
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'productTitle')))
        title_element = driver.find_element(By.ID, 'productTitle')
        title = title_element.text.strip()

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        price_whole = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'a-price-whole'))
        ).text.strip()

        price_fraction = driver.find_element(By.CLASS_NAME, 'a-price-fraction').text.strip()

        price = float(price_whole.replace(',', '') + '.' + price_fraction)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
    return price, title

def send_confirmation_email(user_email, prod_title, price_wanted):
    subject = "Amazon Price Tracking Subscription Confirmation"
    body = f'Congrats! You have successfully subscribed to be notified when the following product "{prod_title}" reaches your desired price of ${price_wanted:.2f}.\n\nYou will receive an email once the price is met or dropped below your desired price.'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "amazonify.pricealert@gmail.com"
    msg['To'] = user_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login("amazonify.pricealert@gmail.com", "lntu xgmj dwnl rnxh")

    server.sendmail(msg['From'], [msg['To']], msg.as_string())

    server.quit()

def send_notification(url, price_wanted, user_email, actual_price, prod_title):
    subject = "Amazon Price Alert"
    body = f'The product you enlisted for is: {prod_title}\n\nYour desired price for this item was ${price_wanted:.2f} and it has been reached with the current price of ${actual_price}\n\nWould you like to purchase this item now?\n\nFollow this link: {url}\n\nMail sent from Amazonify (DO NOT REPLY)'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "amazonify.pricealert@gmail.com"
    msg['To'] = user_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login("amazonify.pricealert@gmail.com", "lntu xgmj dwnl rnxh")

    server.sendmail(msg['From'], [msg['To']], msg.as_string())

    server.quit()

if __name__ == "__main__":
    app.run(debug=True)