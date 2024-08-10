# Notes
'''
Base URL is the same for Amazon
Product ID can be extracted through user's inputted URL
Schedule the track prices function (minutely, hourly, etc.) using the schedule library
'''

# imports (using selenium, time, and schedule)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from email.mime.text import MIMEText
import smtplib
import time
import schedule

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

# URL of the Amazon product (get from user input)
# url = "https://www.amazon.com/Twister-Science-Tornadoes-Making-adventure/dp/0671000292/ref=m_crc_dp_lf_d_t1_d_sccl_2_6/132-6584591-3773905?pd_rd_w=GMp7i&content-id=amzn1.sym.a5144f00-3d78-40a4-aa84-7ff51eea31f7&pf_rd_p=a5144f00-3d78-40a4-aa84-7ff51eea31f7&pf_rd_r=G8CY67CAQ24F8HDQWAEE&pd_rd_wg=I2gnL&pd_rd_r=766d4ac2-db14-420f-ad2f-f8c65edf755b&pd_rd_i=0671000292&psc=1"

def get_input():
    URL = input("Enter URL for the Amazon product you would like to track prices for: ")
    price_input = float(input("Enter your desired price for this product: "))
    email_input = input("Enter your Email Address: ")
    #print(URL, '/n', price_input)
    return URL, price_input, email_input

# scraping product price
# input: url
# output: prints product title and price
def scrape_amazon_price(url):
    price, title = None, None  # Initialize variables
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'productTitle')))
        title_element = driver.find_element(By.ID, 'productTitle')
        title = title_element.text.strip()

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1) 
        
        price_whole = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'a-price-whole'))
        ).text.strip()

        price_fraction = driver.find_element(By.CLASS_NAME, 'a-price-fraction').text.strip()

        price = float(price_whole.replace(',', '') + '.' + price_fraction)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
    return price, title


# scrape_amazon_price(url)


def send_notification(url, price_wanted, user_email, actual_price, prod_title):
    subject = "Amazon Price Alert"
    body = f'The product you enlisted for is {prod_title}\n\nYour desired price for this item was ${price_wanted} and it has been reached with the current price of ${actual_price}\n\nWould you like to purchase this item now?\n\nFollow this link: {url}\n\nMail sent from Amazonify (DO NOT REPLY)'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "amazonify.pricealert@gmail.com"
    msg['To'] = user_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login("amazonify.pricealert@gmail.com", "lntu xgmj dwnl rnxh")

    server.sendmail(msg['From'], [msg['To']], msg.as_string())

    server.quit()

# send_notification()

def track_price():
    url, price_wanted, user_email = get_input()
    actual_price, prod_title = scrape_amazon_price(url)
    print(f'This is the actual price:{actual_price} and this is title:{prod_title}')
    if actual_price <= price_wanted:
        send_notification(url, price_wanted, user_email, actual_price, prod_title)
    else:
        # Optionally, you can log or update something here
        pass


# Schedule the task every hour
# schedule.every().hour.do(track_price)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

track_price()


