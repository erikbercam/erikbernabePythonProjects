import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL del sitio sugerido en la práctica 
URL = "http://books.toscrape.com/"

print("Iniciando el proceso de scraping...")

try:
    # 1. Realizar la petición a la web
    response = requests.get(URL)
    response.raise_for_status()  # Lanza un error si la petición falla

    # 2. Parsear el HTML con BeautifulSoup 
    soup = BeautifulSoup(response.content, 'html.parser')

    # Lista para guardar los datos
    books_data = []

    # 3. Encontrar todos los libros.
    # Cada libro está en un <article class="product_pod">
    books = soup.find_all('article', class_='product_pod')

    # 4. Extraer la información de cada libro [cite: 11]
    for book in books:
        # Extraer Título (está en el atributo 'title' de un enlace <a> dentro de un <h3>) 
        title = book.h3.a['title']

        # Extraer Precio (está en el texto de un <p class="price_color">) 
        price = book.find('p', class_='price_color').text

        # Extraer Rating (está en la segunda clase de <p class="star-rating Three">) 
        # 'class' devuelve una lista, ej: ['star-rating', 'Three']. Queremos el segundo elemento.
        rating = book.find('p', class_='star-rating')['class'][1]

        # Añadir los datos a nuestra lista
        books_data.append({
            'Title': title,
            'Price': price,
            'Rating': rating
        })

    # 5. Guardar la información en un archivo CSV con Pandas 
    df = pd.DataFrame(books_data)
    df.to_csv('books.csv', index=False, encoding='utf-8')

    print(f"¡Éxito! Se han extraído y guardado {len(df)} libros en 'books.csv'.")

except requests.exceptions.RequestException as e:
    print(f"Error: No se pudo conectar a la página web. {e}")
except Exception as e:
    print(f"Ha ocurrido un error inesperado: {e}")