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
    aves_vivas = (df_lotes['cantidad'].sum() if not df_lotes.empty else 0) - (df_bajas['cantidad'].sum() if not df_bajas.empty else 0)
    pienso = df_gastos['ilos_pienso'].sum() if not df_gastos.empty else 0
    consumo_dia = aves_vivas * 0.125
    if temp>30: consumo_dia*=1.15
    autonomia = int(pienso/consumo_dia) if consumo_dia>0 else 0
    return autonomia, consumo_dia