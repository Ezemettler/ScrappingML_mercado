import requests
from bs4 import BeautifulSoup

enlace = "https://www.mercadolibre.com.ar/lampara-colgante-de-techo-tikka-masala-diamante-algodon/p/MLA28053289"

respuesta = requests.get(enlace)
soup = BeautifulSoup(respuesta.text, "html.parser")

precios = soup.find_all("span", class_="andes-money-amount__fraction")
precio_final = None

if precios:
    for precio in precios:
        if not precio.find_parent("s"):
            precio_final = precio.text.strip()
            break

print(f"Precio final: {precio_final}")
