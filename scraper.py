import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "http://books.toscrape.com/"
print(f"Iniciando el scraping de {URL}")

response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")

lista_de_libros = []

libros = soup.find_all('article', class_="product_pod")

for libro in libros:
    titulo = libro.h3.a['title']
    precio_texto = libro.find('p', class_='price_color').text
    rating = libro.find('p', class_='star-rating')['class'][1]

    datos_libros = {
        "titulo": titulo,
        "precio": precio_texto,
        "rating": rating
    }

    lista_de_libros.append(datos_libros)


df = pd.DataFrame(lista_de_libros)
df.to_csv("libros.csv", index=False)

print(f"Scraping completado. Se guardaron {len(df)} libros en 'libros.csv'.")


