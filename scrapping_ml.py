import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def obtener_titulo_publicacion(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Obtener título de la publicación
    titulo_elem = soup.find('h1', class_='ui-pdp-title')    
    titulo = titulo_elem.text.strip() if titulo_elem else 'No encontrado'

    # Obtener puntaje
    puntaje_elem = soup.find('span', class_='ui-pdp-review__rating')
    puntaje = puntaje_elem.text.strip() if puntaje_elem else 'No encontrado'

    # Obtener cantidad de reseñas
    cant_resenias_elem = soup.find('span', class_='ui-pdp-review__amount')
    cant_resenias = cant_resenias_elem.text.strip() if cant_resenias_elem else 'No encontrado'

    # Obtener precio
    precio_elem = soup.find('span', class_='andes-money-amount__fraction')
    precio = precio_elem.text.strip() if precio_elem else 'No encontrado'  

    # Obtener vendedor
    vendedor_elem = soup.find('span', class_='ui-pdp-seller__label-sold')
    vendedor = vendedor_elem.text.strip() if vendedor_elem else 'No encontrado'  

    
    
    return titulo, puntaje, cant_resenias, precio, vendedor

def main(productos_urls):
    datos = []
    
    for producto, url in productos_urls:
        titulo, puntaje, cant_resenias, precio, vendedor = obtener_titulo_publicacion(url)
        datos.append([producto, url, titulo, puntaje, cant_resenias, precio, vendedor])
        time.sleep(1)  # Esperar 2 segundos entre cada solicitud para no sobrecargar el servidor
    
    # Crear un DataFrame con los datos obtenidos
    df = pd.DataFrame(datos, columns=['Producto', 'Link', 'Titulo', 'Puntaje', 'Cant reseñas', 'Precio', 'Vendido por'])
    
    # Guardar el DataFrame en un archivo CSV
    #df.to_csv('titulos_lamparas.csv', index=False)
    print(df)

# Lista de productos y sus URLs de ejemplo
productos_urls = [
    ('Lámpara Berna 30cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1159153997-lampara-colgante-rustico-hilo-yute-diamante-chica-_JM')
    # Agregar más tuplas de producto y URL según sea necesario
]

if __name__ == "__main__":
    main(productos_urls)
