#First Test Script 
#Testing 2

from bs4 import BeautifulSoup
import requests

url = "https://www.cargurus.com/"

page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="main")
#print(results.prettify())
element_names = results.find_all("div", class_="tab-content")
print(element_names)
