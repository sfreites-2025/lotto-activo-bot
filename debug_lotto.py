import requests
from bs4 import BeautifulSoup

url = "https://lotoven.com/animalitos/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

try:
    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    print("--- BUSCANDO CONTENEDORES CON 'LOTTO' EN LOTOVEN ---")
    coincidencias = soup.find_all(string=lambda t: t and 'lotto' in t.lower())
    
    if not coincidencias:
        print("No se encontraron elementos con la palabra 'lotto' en el HTML.")
    
    for i, elem in enumerate(coincidencias[:5]):
        padre = elem.parent
        bloque = padre.find_parent()
        print(f"[{i+1}] Etiqueta: <{padre.name}> | Clase: {padre.get('class')}")
        print(f"    Texto: {elem.strip()}")
        if bloque:
            print(f"    Contenido cercano: {bloque.get_text(separator=' ', strip=True)[:180]}...\n")

except Exception as e:
    print(f"Error al conectar: {e}")