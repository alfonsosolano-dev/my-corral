import pandas as pd
import sqlite3

CONFIG_IA = {
    "Roja": {"puesta": 0.92, "cons": 0.120, "madurez": 126, "consejo": "Alta puesta. Requiere calcio extra."},
    "Blanca": {"puesta": 0.88, "cons": 0.115, "madurez": 130, "consejo": "Muy activa. Necesita espacio."},
    "Mochuela": {"puesta": 0.80, "cons": 0.100, "madurez": 140, "consejo": "Rústica. Ideal para exterior."},
    "Broiler": {"madurez": 50, "cons": 0.180, "consejo": "Crecimiento rápido. Vigilar patas."},
    "Campero": {"madurez": 85, "cons": 0.150, "consejo": "Carne de calidad. Ciclo medio."},
    "Codorniz": {"puesta": 0.75, "cons": 0.035, "madurez": 45, "consejo": "Ciclo muy rápido."}
}

DB_PATH = "corral_maestro_pro.db"

def cargar_datos(tabla):
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        return pd.read_sql(f"SELECT * FROM {tabla}", conn)
    except:
        return pd.DataFrame()

def get_clima_cartagena(api_key):
    import requests
    if not api_key: return 22.0
    try:
        url = f"https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/7012D?api_key={api_key}"
        r = requests.get(url, timeout=5).json()
        datos = requests.get(r["datos"], timeout=5).json()
        return float(datos[-1]["ta"])
    except:
        return 22.0

def calcular_autonomia(df_lotes, df_bajas, df_gastos, temp):
    import pandas as pd
    from datetime import datetime

    if df_lotes.empty:
        return 0, 0

    # 1. Calcular aves vivas por lote y su consumo dinámico
    consumo_total_diario = 0
    
    for _, lote in df_lotes.iterrows():
        # Calcular aves actuales en este lote
        bajas_lote = df_bajas[df_bajas['lote'] == lote['id']]['cantidad'].sum() if not df_bajas.empty else 0
        aves_vivas = lote['cantidad'] - bajas_lote
        
        if aves_vivas <= 0: continue

        # Calcular edad actual (días)
        fecha_inicio = pd.to_datetime(lote['fecha'])
        edad_actual = (datetime.now() - fecha_inicio).days + lote['edad_inicial']
        
        # --- Lógica de Consumo por Especie ---
        especie = lote['especie']
        
        if especie == "Broiler":
            # Crecimiento rápido: de 50g a 180g según edad (aprox)
            consumo_base = min(0.050 + (edad_actual * 0.003), 0.180)
        elif especie == "Codorniz":
            consumo_base = 0.035
        else: # Ponedoras (Roja, Blanca, etc.)
            # Suben de 80g a 120g al llegar a la madurez
            consumo_base = min(0.080 + (edad_actual * 0.0005), 0.125)

        consumo_total_diario += (aves_vivas * consumo_base)

    # 2. Ajuste por temperatura (Cartagena)
    if temp > 30: 
        consumo_total_diario *= 1.15  # Comen/beben más con calor
    elif temp < 10:
        consumo_total_diario *= 1.10  # Gastan más energía para calor

    # 3. Stock de pienso (Suma de todos los sacos registrados)
    stock_pienso = df_gastos['ilos_pienso'].sum() if not df_gastos.empty else 0
    
    # 4. Cálculo de autonomía
    autonomia = int(stock_pienso / consumo_total_diario) if consumo_total_diario > 0 else 0
    
    return autonomia, consumo_total_diario