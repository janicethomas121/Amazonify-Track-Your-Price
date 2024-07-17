#First Test Script 
#Testing 2

from bs4 import BeautifulSoup
import requests

URL = "https://www.kbb.com/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="homeBestCars")
print(results.prettify())

