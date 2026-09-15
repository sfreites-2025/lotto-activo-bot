# 🎲 Lotto Activo - Bot de Pronósticos y Monitoreo en Vivo

Bot interactivo desarrollado en Python para el seguimiento en tiempo real y análisis estadístico de los resultados del juego **Lotto Activo**. El sistema construye progresivamente un historial en una base de datos SQLite local para calcular los "Fijos del Día" con mayor probabilidad de salida.

---

## 🚀 Características Principales

* **📦 Base de Datos Acumulativa:** Guarda de forma permanente cada sorteo en SQLite (`lotto_activo.db`). El historial jamás se borra y nutre el algoritmo día a día.
* **🎯 Algoritmo de Pronóstico:** Analiza las frecuencias históricas de los sorteos acumulados para proyectar los 6 números principales (*Fijos del Día*) antes de iniciar la jornada.
* **🔍 Scraping Inteligente:** Extrae los resultados en vivo desde la web filtrando exclusivamente las tarjetas oficiales de Lotto Activo para evitar cruzado de datos con otras loterías.
* **📋 Tablero Fijo de 12 Horarios:** Organiza la parrilla diaria desde las **08:00 AM** hasta las **07:00 PM**, mostrando qué números salieron y cuáles faltan por salir.
* **🌅 Cambio Automático de Jornada:** Detecta el cambio de fecha a medianoche, guarda el día finalizado y resetea el panel con los nuevos pronósticos del día entrante.

---

## 📊 Vista del Panel de Control (CLI)

```text
═════════════════════════════════════════════════════════════════
 📊 PANEL DIARIO LOTTO ACTIVO | FECHA: 2026-09-09
 📦 Historial Registrado: 844 sorteos en base de datos
═════════════════════════════════════════════════════════════════

 🎯 PRONÓSTICO DEL DÍA (FIJOS CALCULADOS):
   🟢 [02] TORO       ──► ¡ACERTADO! (Salió a las 08:00 AM) ✅
   ⏳ [10] TIGRE      ──► PENDIENTE POR SALIR
   ⏳ [32] ARDILLA    ──► PENDIENTE POR SALIR
   ⏳ [11] GATO       ──► PENDIENTE POR SALIR
   ⏳ [27] PERRO      ──► PENDIENTE POR SALIR
   ⏳ [18] BURRO      ──► PENDIENTE POR SALIR

 📈 Aciertos de hoy: 1 de 6
-----------------------------------------------------------------
 📋 TABLERO OFICIAL DEL DÍA (8:00 AM a 7:00 PM):
   • 08:00 AM ──► [02] TORO       🎯 [FIJO DEL DÍA]
   • 09:00 AM ──► [05] LEÓN       
   • 10:00 AM ──► [03] CIEMPIÉS   
   • 11:00 AM ──► [19] CHIVO      
   • 12:00 PM ──► [ -- ] POR SALIR...
   • ...
═════════════════════════════════════════════════════════════════
