import requests
import re
from bs4 import BeautifulSoup

url = "https://www.lottoactivo.com/resultados/animalitos/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

res = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(res.text, 'html.parser')
texto = soup.get_text()

# Patrón regex exacto para extraer resultados de Lotto Activo
patron = r'(\d{1,2}|00)\s+([A-Za-zÁÉÍÓÚáéíóúñÑ]+)[\.\s]+Lotto Activo\s+(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm))'
coincidencias = re.findall(patron, texto, re.IGNORECASE)

print(f"--- RESULTADOS EXTRAÍDOS ({len(coincidencias)} SORTEOS) ---")
for num, animal, hora in coincidencias:
    print(f"Hora: {hora.upper()} | Número: {num.zfill(2)} | Animal: {animal}")