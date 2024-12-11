from bs4 import BeautifulSoup
import requests
import json

ENDPOINT = "https://books.toscrape.com/catalogue/page-1.html"
html_response = requests.get(ENDPOINT).text

html_soup = BeautifulSoup(html_response, 'html.parser')
products = html_soup.find_all('article', class_='product_pod')
products_data = []
for product in products:
    book_data = {
        'url' : "https://books.toscrape.com/" + product.h3.a['href'],
        'title': product.h3.a['title'],
        'price': product.find('p', class_='price_color').text
    }
    products_data.append(book_data)
    
print(products[0])

with open('books.json', 'w') as f:
    json.dump(products_data, f, ensure_ascii=False, indent=4)