from bs4 import BeautifulSoup
import requests
import json

############## 
'''
a) View the HTML Document

print(soup.prettify()) 

b) 
+ Find a single element:
title = soup.find('title')  # Find the first <title> tag
print(title.text)

+ Find all elements
all_paragraphs = soup.find_all('p')  # Find all <p> tags
for paragraph in all_paragraphs:
    print(paragraph.text)

+ Links: (SPECIAL)
for link in soup.find_all('a', href=True):
    print(link['href'])


+ Find by attributs
div_with_class = soup.find('div', class_='example-class')  # Find <div class="example-class">
specific_id = soup.find(id='unique-id')  # Find by ID
 

c) CSS Selectors
links = soup.select('a[href]')  # Select all links with an href attribute

d) Extract Attributes
link = soup.find('a')
if link:
    print(link['href'])  # Extract the href attribute

e) Navigate the Tree
parent = soup.find('div').parent  # Get the parent
children = soup.find('div').contents  # Get all children

f) Reguler expression
import re
links_with_https = soup.find_all('a', href=re.compile('^https'))
for link in links_with_https:
    print(link['href'])

    
Modify: 
a) Replace Tag Content:
tag = soup.find('p')
tag.string = "New content"

b) Add or Remove Tags:
new_tag = soup.new_tag('span')  # Create a new tag
new_tag.string = "Added Content"
soup.find('div').append(new_tag)  # Append the new tag


c) Delete Tags:
for tag in soup.find_all('script'):  # Remove all <script> tags
    tag.decompose()

d) Saving
with open("output.html", "w", encoding="utf-8") as file:
    file.write(soup.prettify())

    
* Realworl usage: 
url = 'https://example.com'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml')

for link in soup.find_all('a', href=True):
    print(link['href'])

    
Advance Features 
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://example.com')
soup = BeautifulSoup(driver.page_source, 'lxml')
driver.quit()

tables = soup.find_all('table')
for table in tables:
    print(table)

import csv

rows = []
for row in soup.select('table tr'):
    rows.append([cell.text.strip() for cell in row.find_all(['td', 'th'])])

with open('output.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

    


    
NOTE:
USING THIS TO MIMIC A BROWSER: 
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)

'''





ENDPOINT = "https://books.toscrape.com/catalogue/page-1.html"
html_response = requests.get(ENDPOINT).text

html_soup = BeautifulSoup(html_response, 'html.parser')
print(html_soup.title.string)
products = html_soup.find_all('article', class_='product_pod')

products_data = []
for product in products:
    book_data = {
        'url' : "https://books.toscrape.com/" + product.h3.a['href'],
        'title': product.h3.a['title'],
        'price': product.find('p', class_='price_color').text
    }
    products_data.append(book_data)
    
# print(products[0])

with open('books.json', 'w') as f:
    json.dump(products_data, f, ensure_ascii=False, indent=4)