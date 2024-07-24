from bs4 import BeautifulSoup
import requests

base_url = 'https://www.amazon.com'
url = "https://www.amazon.com/dp/B09KY2PMYM"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://www.google.com/'
}

base_response = requests.get(base_url, headers=headers)
cookies = base_response.cookies

product_response = requests.get(url, headers=headers, cookies=cookies)
soup = BeautifulSoup(product_response.text, features='lxml')
price_whole = soup.findAll(class_='a-price-whole')
price_fraction = soup.findAll(class_='a-price-fraction')

if price_whole:
    price_dollar = str(price_whole[0])
    price_dollar = price_dollar.replace('<span class="a-price-whole">', '')
    price_dollar = price_dollar.replace('</span>', '')
    price_dollar = price_dollar.replace('<span class="a-price-decimal">', '')

if price_fraction:
     price_cent = str(price_fraction[0])
     price_cent = price_cent.replace('<span class="a-price-fraction">', '')
     price_cent = price_cent.replace('</span>', '')


print(price_dollar+price_cent)












# def get_user_input():
#     min_price = input("Enter minimum price: ")
#     max_price = input("Enter maximum price: ")
#     zip_code = input("Enter zip code: ")
#     return min_price, max_price, zip_code

# def retrieve_listings(min_price, max_price, zip_code):
#     url = 'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action'
#     params = {
#         'sourceContext': 'carGurusHomePagePrice',
#         'inventorySearchWidgetType': 'PRICE',
#         'minPrice': min_price,
#         'maxPrice': max_price,
#         'zip': zip_code
#     }

#     response = requests.get(url, params=params)

#     if response.status_code == 200:
#         return response.text
#     else:
#         print(f"Failed to retrieve data. Status code: {response.status_code}")
#         return None 

# def parse_url(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
    
#     car_listings = soup.find_all('div', class_='f3fzTi')
    
#     if not car_listings:
#         print("No car listings found.")
#         return

#     for car in car_listings:
#         try:
#             title = car.find('h4', class_='JzvPHo').text.strip()
#             price = car.find('span', class_='f4fcTX').text.strip()
#             details = car.find('div', class_='w4tUoG').text.strip()
            
#             print(f"Title: {title}")
#             print(f"Price: {price}")
#             print(f"Details: {details}")
#             print("-----")
#         except AttributeError:
#             continue

# if __name__ == "__main__":
#     min_price, max_price, zip_code = get_user_input()
#     html_content = retrieve_listings(min_price, max_price, zip_code)
    
#     if html_content:
#         parse_url(html_content)