import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

fecha_test_iso = "2026-09-06"
fecha_test_lat = "06-09-2026"

pruebas = [
    ("Hoy (Lotto Activo)", "GET", "https://lotoven.com/animalito/lottoactivo/resultados/", {}),
    ("Ayer (Lotto Activo)", "GET", "https://lotoven.com/animalito/lottoactivo/resultados/ayer/", {}),
    ("GET Param ISO", "GET", f"https://lotoven.com/animalito/lottoactivo/resultados/?fecha={fecha_test_iso}", {}),
    ("POST Form ISO", "POST", "https://lotoven.com/animalito/lottoactivo/resultados/", {"fecha": fecha_test_iso}),
    ("POST Form LAT", "POST", "https://lotoven.com/animalito/lottoactivo/resultados/", {"fecha": fecha_test_lat}),
]

print("--- PROBANDO RUTA CORRECTA DE LOTOACTIVO EN LOTOVEN ---")
patron = r'(\d{1,2}|00)\s*[\-\.]?\s*([A-Za-zÁÉÍÓÚáéíóúñÑ]+)\s*[\-\.]?\s*(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm))'

for nombre, metodo, url, data in pruebas:
    try:
        if metodo == "GET":
            res = requests.get(url, headers=headers, timeout=10)
        else:
            res = requests.post(url, headers=headers, data=data, timeout=10)
            
        matches = re.findall(patron, res.text)
        print(f"[{nombre}] Status: {res.status_code} | Sorteos extraídos: {len(matches)}")
        if matches:
            print(f"   -> Ejemplo: {matches[0]}")
    except Exception as e:
        print(f"[{nombre}] Error: {e}")