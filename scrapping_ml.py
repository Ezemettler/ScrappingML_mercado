import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def obtener_datos_etiqueta(soup, etiquetas):
    for etiqueta, clase in etiquetas:
        elemento = soup.find(etiqueta, class_=clase)
        if elemento:
            return elemento.text.strip()
    return 'No encontrado'

def obtener_titulo_publicacion(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Obtener título de la publicación
    titulo = obtener_datos_etiqueta(soup, [('h1', 'ui-pdp-title')])
    
    # Obtener puntaje
    puntaje = obtener_datos_etiqueta(soup, [('span', 'ui-pdp-review__rating')])
    if puntaje == 'No encontrado':
        puntaje = 0
    
    # Obtener cantidad de reseñas
    cant_resenias = obtener_datos_etiqueta(soup, [('span', 'ui-pdp-review__amount')]).replace('(', '').replace(')', '')
    if cant_resenias == 'No encontrado':
        cant_resenias = 0
    
    # Obtener precio
    precio = obtener_datos_etiqueta(soup, [('span', 'andes-money-amount__fraction')]).replace('.', '')

    # Obtener envio
    envio = obtener_datos_etiqueta(soup, [('span', 'ui-pdp-color--GREEN ui-pdp-family--SEMIBOLD')]).replace('llega', '')

    #Obtener unidades vendidas
    un_vendidas = obtener_datos_etiqueta(soup, [('span', 'ui-pdp-subtitle')])
    if un_vendidas == 'No encontrado':
        un_vendidas = 0
    else:
        # Usa una expresión regular para extraer el número
        match = re.search(r'\+(\d+)', un_vendidas)
        if match:
            un_vendidas = int(match.group(1))  # Convierte el número a entero
        else:
            un_vendidas = 0  # Si no se encuentra el número, asigna 0
    
    # Obtener vendedor (múltiples clases posibles)
    vendedor = obtener_datos_etiqueta(soup, [('span', 'ui-pdp-color--BLACK ui-pdp-size--LARGE ui-pdp-family--REGULAR ui-seller-data-header__title non-selectable'),
                                             ('span', 'ui-pdp-color--BLACK ui-pdp-size--LARGE ui-pdp-family--SEMIBOLD ui-seller-data-header__title non-selectable')
    ]).replace('Vendido por', '').strip()
    
    ventas = obtener_datos_etiqueta(soup, [('span', 'ui-pdp-color--BLACK ui-pdp-size--XSMALL ui-pdp-family--BOLD')]).replace('ventas', '').strip('+')

    # Obtener categoría
    categoria = obtener_datos_etiqueta(soup, [('p', 'ui-pdp-color--GREEN ui-pdp-size--XSMALL ui-pdp-family--SEMIBOLD ui-seller-data-status__title'),
                                              ('p', 'ui-pdp-color--BLACK ui-pdp-size--XSMALL ui-pdp-family--REGULAR ui-pdp-seller__header__subtitle')])
    
    return titulo, puntaje, cant_resenias, precio, envio, un_vendidas, vendedor, ventas, categoria

def main(productos_urls):
    datos = []
    
    for producto, url in productos_urls:
        titulo, puntaje, cant_resenias, precio, envio, un_vendidas, vendedor, ventas, categoria = obtener_titulo_publicacion(url)
        datos.append([producto, url, titulo, puntaje, cant_resenias, precio, envio, un_vendidas, vendedor, ventas, categoria])
        print('Info extraida sobre producto: ', producto)
        time.sleep(2)  # Esperar 1 segundo entre cada solicitud para no sobrecargar el servidor
    
    # Crear un DataFrame con los datos obtenidos
    df = pd.DataFrame(datos, columns=['Producto', 'Link', 'Titulo', 'Puntaje', 'Cant reseñas', 'Precio', 'Costo envío', 'Un vendidas', 'Vendedor', 'Ventas', 'Categoria'])
    
    # Guardar el DataFrame en un archivo Excel
    df.to_csv('/home/eze-ubuntu/Documents/data_projects/bios/scrapping_ML/mercado_lamparas.csv', index=False)
    print(df)

# Lista de productos y sus URLs de ejemplo
productos_urls = [
    
    ('Lámpara Berna 40cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-852866056-colgante-lampara-vintage-de-yute-iluminacion-1-luz-_JM'),
    ('Lámpara Berna 40cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1174516808-colgante-lampara-vintage-hilo-algodon-color-1-luz-_JM'),
    ('Lámpara Berna 40cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1132524998-lampara-colgante-vintage-hilo-yute-1-luz-_JM'),
    ('Lámpara Berna 40cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-867647684-lampara-colgante-premium-hilo-yute-40x30-altura-_JM'),
    ('Lámpara Berna 40cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1136327844-lampara-colgante-hilo-yute-diamante-apto-luz-led-_JM'),
    ('Lámpara Berna 40cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1159047111-lampara-colgante-rustico-hilo-yute-diamante-_JM')
]
'''
('Lámpara Berna 30cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1159153997-lampara-colgante-rustico-hilo-yute-diamante-chica-_JM'),
('Lámpara Berna 30cm Natural', 'https://articulo.mercadolibre.com.ar/MLA-1128223183-lampara-colgante-hilo-diamante-chico-colores-alto-26-cms-_JM'),
('Lámpara Berna 30cm Natural', 'https://articulo.mercadolibre.com.ar/MLA-1122042407-lampara-colgante-hilo-diamante-chico-alto-26-cms-_JM'),
('Lámpara Berna 30cm Natural', 'https://articulo.mercadolibre.com.ar/MLA-1159160464-lampara-colgante-macrame-hilo-algodon-diamante-natural-chica-_JM'),
('Lámpara Berna 40cm Natural', 'https://articulo.mercadolibre.com.ar/MLA-852868382-colgante-lampara-vintage-hilo-natural-iluminacion-1-luz-_JM'),
('Lámpara Berna 40cm Natural', 'https://articulo.mercadolibre.com.ar/MLA-877355404-colgante-hilo-natural-40cm-apto-led-deco-luz-desing-_JM'),
('Lámpara Berna 40cm Natural', 'https://www.mercadolibre.com.ar/lampara-de-techo-tikka-masala-diamante-algodon-color-natural-220v/p/MLA28053289'),
('Lámpara Berna 40cm Natural', 'https://articulo.mercadolibre.com.ar/MLA-1132524998-lampara-colgante-vintage-hilo-yute-1-luz-_JM'),
('Lámpara Berna 40cm Natural', 'https://articulo.mercadolibre.com.ar/MLA-1174516808-colgante-lampara-vintage-hilo-algodon-color-1-luz-_JM'),
('Lámpara Berna 40cm Natural', 'https://articulo.mercadolibre.com.ar/MLA-1159015021-lampara-colgante-macrame-hilo-algodon-diamante-natural-_JM'),
('Lámpara Berna 50cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1135299325-lampara-colgante-vintage-hilo-yute-1-luz-modelo-grande-_JM'),
('Lámpara Berna 50cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1390404895-lampara-colgante-rustico-hilo-yute-diamante-grande-_JM'),
('Lámpara Berna 50cm Natural', 'https://articulo.mercadolibre.com.ar/MLA-1158032242-lampara-colgante-hilo-natural-algodon-diamante-50cm-luz-led-_JM'),
('Lámpara Berna 50cm Natural', 'https://articulo.mercadolibre.com.ar/MLA-1375768929-lampara-colgante-hilo-algodon-diamante-50cm-luz-led-_JM'),
('Lámpara Berna 50cm Natural', 'https://articulo.mercadolibre.com.ar/MLA-1159161081-lampara-colgante-macrame-hilo-algodon-diamante-natural-grand-_JM'),
('Lámpara Bella 30cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1176210134-lampara-colgante-tambor-hilo-yute-1-luz-modelo-chico-30cm-_JM'),
('Lámpara Bella 30cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1175819983-lampara-colgante-vintage-hilo-algodon-color-1-luz-_JM'),
('Lámpara Bella 30cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1159154855-lampara-colgante-rustico-hilo-yute-redonda-chica-_JM'),
('Lámpara Bella 30cm Natural', 'https://articulo.mercadolibre.com.ar/MLA-1176210134-lampara-colgante-tambor-hilo-yute-1-luz-modelo-chico-30cm-_JM'),
('Lámpara Bella 30cm Natural', 'https://articulo.mercadolibre.com.ar/MLA-1175819983-lampara-colgante-vintage-hilo-algodon-color-1-luz-_JM'),
('Lámpara Bella 30cm Natural', 'https://articulo.mercadolibre.com.ar/MLA-1107174705-lampara-colgante-de-algodon-natural-30cm-diam-modelo-bella-_JM'),
('Lámpara Bella 40cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1174312904-lampara-colgante-tambor-hilo-yute-1-luz-modelo-grande-_JM'),
('Lámpara Bella 40cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1159200288-lampara-colgante-rustico-hilo-yute-redonda-_JM'),
('Lámpara Bella 40cm Natural', 'https://articulo.mercadolibre.com.ar/MLA-852864795-lampara-colgante-vintage-hilo-natural-1-luz-apto-led-_JM'),
('Lámpara Bella 50cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-736206110-lamparas-colgantes-rusticas-cocina-comedor-50cm-moderna-led-_JM'),
('Lámpara Bella 50cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1505838632-lampara-colgante-tambor-hilo-yute-grande-50cm-x-20cm-alto-_JM'),
('Lámpara Bella 50cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1146441891-lampara-colgante-hilo-algodon-natural-negro-yute-50cm-tambor-_JM'),
('Lámpara Bella 50cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1302516110-lampara-colgante-hilo-yute-modelo-conica-35x45x25-alto-_JM'),
('Lámpara Lucerna 40cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1372026915-lamparas-de-fibras-naturales-rustica-de-yute-galponera-_JM'),
('Pantalla Pie Bella 40cm', 'https://articulo.mercadolibre.com.ar/MLA-1139461180-pantallas-para-iluminacion-lampara-de-pie-_JM'),
('Pantalla Pie Bella 40cm', 'https://articulo.mercadolibre.com.ar/MLA-1470627438-pantalla-para-lampara-de-pie-tambor-40cm-x-25cm-alto-_JM'),
('Pantalla Pie Bella 40cm', 'https://articulo.mercadolibre.com.ar/MLA-854563256-pantalla-tambor-para-veladorpie-4025-arpillera-o-lino-_JM'),
('Pantalla Pie Bella 40cm', 'https://articulo.mercadolibre.com.ar/MLA-875183930-pantalla-para-lampara-de-pie-modelo-conica-30x40x30-alto-_JM'),
('Pantalla Pie Bella 40cm', 'https://articulo.mercadolibre.com.ar/MLA-779554664-pantalla-para-lampara-de-pie-45-45-2-0-cm-alt-arpillera-pr-_JM'),
('Pantalla Pie Bella 40cm', 'https://articulo.mercadolibre.com.ar/MLA-1360864255-pantalla-velador-lampara-de-pie-forma-circular-yute-rustica-_JM'),
('Lámpara Cónica 40cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1345722239-lampara-hilo-sisal-colgante-campana-nro2-tostado-claro-_JM'),
('Lámpara Cónica 40cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-643876871-lamparas-de-techo-modernas-colgante-comedor-_JM'),
('Lámpara Cónica 40cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1372157781-lampara-conica-colgante-rustica-de-hilo-de-yute-luz-led-_JM'),
('Lámpara Cónica 40cm Natural', 'https://articulo.mercadolibre.com.ar/MLA-1141620359-lampara-colgante-conica-40cm-hilo-algodon-apto-luz-led-_JM'),
('Lámpara Cónica 40cm Natural', 'https://articulo.mercadolibre.com.ar/MLA-1344997819-colgante-hilo-natural-conico-40cm-apto-led-deco-_JM'),
('Lámpara Cónica 50cm Natural', 'https://articulo.mercadolibre.com.ar/MLA-821476126-lampara-colgante-premium-hilo-yute-algodon-sintetico-_JM'),
('Lámpara Cónica 50cm Natural', 'https://articulo.mercadolibre.com.ar/MLA-882675601-lampara-colgante-conica-de-hilo-yute-premium-a-medida-_JM'),
('Lámpara Ondulada 40cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1155471292-lampara-colgante-premium-ondulada-hiloyutekraft-40cm-_JM'),
('Lámpara Ondulada 40cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1256866095-lampara-colgante-pro-ondulada-hiloyutekraft-40cm-kit-elect-_JM'),
('Lámpara Ondulada 40cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1298755799-lampara-colgante-hilo-yute-modelo-flor-40cm-diametro-_JM'),
('Lámpara Ondulada 40cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1398577593-lampara-colgante-rustica-hilo-yute-ondulada-_JM'),
('Lámpara Ondulada 50cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1155434357-lampara-colgante-premium-ondulada-50cm-hiloyutekraft-_JM'),
('Lámpara Ondulada 60cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1220870341-lampara-colgante-ondulada-personalizada-hiloyute-60cm-_JM'),
('Lámpara Ondulada 60cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1155471309-lampara-colgante-premium-ondulada-hiloyutekraft-60cm-_JM'), 
('Lámpara Ondulada 60cm Yute', 'https://articulo.mercadolibre.com.ar/MLA-1298807517-lampara-colgante-hilo-yute-modelo-flor-grande-60-cm-diametro-_JM')
'''
# Agregar más tuplas de producto y URL según sea necesario

if __name__ == "__main__":
    main(productos_urls)
