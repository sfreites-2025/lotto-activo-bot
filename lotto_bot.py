import sqlite3
import requests
from bs4 import BeautifulSoup
import re
import datetime
import time
import pandas as pd

ANIMALES = {
    "0": "Delfín", "00": "Ballena", "1": "Carnero", "2": "Toro", "3": "Ciempiés",
    "4": "Alacrán", "5": "León", "6": "Rana", "7": "Perico", "8": "Ratón",
    "9": "Águila", "10": "Tigre", "11": "Gato", "12": "Caballo", "13": "Mono",
    "14": "Paloma", "15": "Zorro", "16": "Oso", "17": "Pavo", "18": "Burro",
    "19": "Chivo", "20": "Cochino", "21": "Gallo", "22": "Camello", "23": "Cebra",
    "24": "Iguana", "25": "Gallina", "26": "Vaca", "27": "Perro", "28": "Zamuro",
    "29": "Elefante", "30": "Caimán", "31": "Lapa", "32": "Ardilla", "33": "Pescado",
    "34": "Venado", "35": "Jirafa", "36": "Culebra"
}

HORAS_OFICIALES = [
    "08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
    "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM", 
    "06:00 PM", "07:00 PM"
]

DB_NAME = "lotto_activo.db"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sorteos (
            fecha TEXT, hora TEXT, numero TEXT, animal TEXT, PRIMARY KEY (fecha, hora)
        )
    ''')
    conn.commit()
    conn.close()

def purgar_dia_actual(fecha):
    """Elimina datos viciados de la base de datos para el dia en curso"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sorteos WHERE fecha = ?", (fecha,))
    conn.commit()
    conn.close()

def guardar_sorteo(fecha, hora, numero, animal):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    insertado = False
    try:
        cursor.execute("INSERT OR REPLACE INTO sorteos VALUES (?, ?, ?, ?)", (fecha, hora, numero, animal))
        if cursor.rowcount > 0:
            insertado = True
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()
    return insertado

def cargar_historico():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM sorteos ORDER BY fecha ASC, hora ASC", conn)
    conn.close()
    return df

def formatear_hora(hora_str):
    hora_clean = hora_str.upper().strip()
    if len(hora_clean.split(':')[0]) == 1:
        hora_clean = '0' + hora_clean
    return hora_clean if hora_clean in HORAS_OFICIALES else None

def obtener_sorteos_web(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code != 200: return []
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 1. Filtra los bloques HTML buscando la seccion exclusiva de Lotto Activo
        texto_pagina = soup.get_text(separator='\n', strip=True)
        lineas = [l.strip() for l in texto_pagina.split('\n') if l.strip()]
        
        # Buscar el indice donde empieza Lotto Activo
        inicio_lotto = -1
        for i, linea in enumerate(lineas):
            if "lotto activo" in linea.lower() and "resultados" in linea.lower():
                inicio_lotto = i
                break
        
        # Si no halla el encabezado exacto, toma desde la primera mencion de 'lotto activo'
        if inicio_lotto == -1:
            for i, linea in enumerate(lineas):
                if "lotto activo" in linea.lower():
                    inicio_lotto = i
                    break

        bloque_interes = lineas[inicio_lotto:] if inicio_lotto != -1 else lineas
        texto_filtrado = " ".join(bloque_interes)

        # 2. Extrae las coincidencias dentro de ese bloque aislado
        patron = r'(\d{1,2}|00)\s+([A-Za-zÁÉÍÓÚáéíóúñÑ]+)\s+(?:LOTTO\s+ACTIVO\s+)?(\d{1,2}:00\s*(?:AM|PM))'
        coincidencias = re.findall(patron, texto_filtrado, re.IGNORECASE)
        
        resultados = []
        vistos = set()

        for num, animal_web, hora in coincidencias:
            num_clean = num if num in ["0", "00"] else num.zfill(2)
            hora_norm = formatear_hora(hora)
            
            if num_clean in ANIMALES and hora_norm and hora_norm not in vistos:
                vistos.add(hora_norm)
                resultados.append((hora_norm, num_clean, ANIMALES[num_clean]))
        return resultados
    except Exception:
        return []

def obtener_fijos_del_dia(df, fecha_hoy):
    df_previo = df[df['fecha'] < fecha_hoy]
    if df_previo.empty:
        df_previo = df

    frecuencias = df_previo['numero'].value_counts()
    return frecuencias.head(6).index.tolist()

def renderizar_tablero_y_pronostico(fecha_hoy):
    df = cargar_historico()
    if df.empty: return

    df_hoy = df[df['fecha'] == fecha_hoy]
    sorteos_map = {row['hora']: (row['numero'], row['animal']) for _, row in df_hoy.iterrows()}
    salidos_hoy = set(df_hoy['numero'].tolist())
    fijos_dia = obtener_fijos_del_dia(df, fecha_hoy)

    print("\n" + "═"*65)
    print(f" 📊 PANEL DIARIO LOTTO ACTIVO | FECHA: {fecha_hoy}")
    print(f" 📦 Historial Registrado: {len(df)} sorteos en base de datos")
    print("═"*65)

    print("\n 🎯 PRONÓSTICO DEL DÍA (FIJOS CALCULADOS):")
    aciertos = 0
    for num in fijos_dia:
        n_fmt = num if num in ["0", "00"] else num.zfill(2)
        nombre = ANIMALES[num].upper()
        if num in salidos_hoy:
            hora_salida = df_hoy[df_hoy['numero'] == num]['hora'].values[0]
            print(f"   🟢 [{n_fmt}] {nombre.ljust(10)} ──► ¡ACERTADO! (Salió a las {hora_salida}) ✅")
            aciertos += 1
        else:
            print(f"   ⏳ [{n_fmt}] {nombre.ljust(10)} ──► PENDIENTE POR SALIR")

    print(f"\n 📈 Aciertos de hoy: {aciertos} de {len(fijos_dia)}")
    print("-" * 65)

    print(" 📋 TABLERO OFICIAL DEL DÍA (8:00 AM a 7:00 PM):")
    for h in HORAS_OFICIALES:
        if h in sorteos_map:
            num, animal = sorteos_map[h]
            n_fmt = num if num in ["0", "00"] else num.zfill(2)
            es_fijo = "🎯 [FIJO DEL DÍA]" if num in fijos_dia else ""
            print(f"   • {h} ──► [{n_fmt}] {animal.upper().ljust(10)} {es_fijo}")
        else:
            print(f"   • {h} ──► [ -- ] POR SALIR...")

    print("═"*65 + "\n")

def ciclo_principal():
    inicializar_db()
    fecha_actual = datetime.date.today().strftime("%Y-%m-%d")

    # Limpia datos corruptos en la BD para el dia de hoy
    purgar_dia_actual(fecha_actual)

    # Carga inicial limpia
    for h, n, a in obtener_sorteos_web("https://lotoven.com/animalitos/"):
        guardar_sorteo(fecha_actual, h, n, a)

    renderizar_tablero_y_pronostico(fecha_actual)

    while True:
        ahora = datetime.datetime.now()
        fecha_loop = ahora.strftime("%Y-%m-%d")

        if fecha_loop != fecha_actual:
            fecha_actual = fecha_loop
            purgar_dia_actual(fecha_actual)
            renderizar_tablero_y_pronostico(fecha_actual)

        if 7 <= ahora.hour <= 19:
            sorteos = obtener_sorteos_web("https://lotoven.com/animalitos/")
            nuevos = sum(1 for h, n, a in sorteos if guardar_sorteo(fecha_actual, h, n, a))
            
            if nuevos > 0:
                print(f"[{ahora.strftime('%H:%M:%S')}] 🔔 ¡Sorteo registrado!")
                renderizar_tablero_y_pronostico(fecha_actual)

            time.sleep(1800)
        else:
            time.sleep(1800)

if __name__ == "__main__":
    ciclo_principal()