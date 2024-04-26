import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

books = []

# Loop through all 50 Sites
for i in range(1,51):

    # Target URL
    url = f'http://books.toscrape.com/catalogue/page-{i}.html'

    # Headers to masquerade as a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # Download page HTML using requests
    response = requests.get(url, headers=headers)

    # Check if valid response received
    if response.status_code == 200:

        # Parse HTML using Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')

        # CSS selector for the main list
        table = soup.find('ol')

        # Find all books
        articles = table.find_all('article', class_='product_pod')

        # Loop through every Book
        for article in articles:
            image = article.find('img')
            title = image.attrs['alt']

            stars = article.find('p')
            stars = stars['class'][1]

            price = article.find('p', class_='price_color').text
            price = float(price[2:])

            # Saving Data to our multidimensional Array
            books.append([title, stars, price])

    else:
        print(response.status_code)

# Saving the Data as CSV
df = pd.DataFrame(books, columns=['Title', 'Price €', 'Star Rating'])
df.to_csv('books.csv')