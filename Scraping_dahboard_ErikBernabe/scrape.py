import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "http://books.toscrape.com/"

print("Iniciando el proceso de scraping...")

try:

    response = requests.get(URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    books_data = []

    books = soup.find_all('article', class_='product_pod')


    for book in books:

        title = book.h3.a['title']

        price = book.find('p', class_='price_color').text

        rating = book.find('p', class_='star-rating')['class'][1]

        books_data.append({
            'Title': title,
            'Price': price,
            'Rating': rating
        })

    df = pd.DataFrame(books_data)
    df.to_csv('books.csv', index=False, encoding='utf-8')

    print(f"Se han extraido y guardado {len(df)} libros en 'books.csv'.")

except requests.exceptions.RequestException as e:
    print(f"Error al conectar {e}")
except Exception as e:
    print(f"Error inesperado: {e}")