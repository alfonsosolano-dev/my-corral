import pandas as pd
from datetime import datetime
from db.db import get_conn

def cargar_datos(tabla):
    try:
        with get_conn() as conn:
            return pd.read_sql(f"SELECT * FROM {tabla}", conn)
    except:
        return pd.DataFrame()

def obtener_estado_pienso(df_lotes, df_bajas, df_gastos):
    if df_gastos.empty:
        return 0.0, 0.0, {}
    
    total_comprado = df_gastos['ilos_pienso'].sum() if 'ilos_pienso' in df_gastos.columns else 0
    consumo_acumulado_total = 0
    consumo_por_especie = {}

    if not df_lotes.empty:
        for _, lote in df_lotes.iterrows():
            bajas = df_bajas[df_bajas['lote'] == lote['id']]['cantidad'].sum() if not df_bajas.empty else 0
            vivas = lote['cantidad'] - bajas
            if vivas <= 0: continue

            fecha_lote = pd.to_datetime(lote['fecha'])
            dias_totales = (datetime.now() - fecha_lote).days
            
            especie = str(lote['especie'])
            consumo_lote = 0

            for d in range(max(0, dias_totales) + 1):
                edad_dia = lote['edad_inicial'] + d
                esp_lower = especie.lower()
                if "pollo" in esp_lower or "broiler" in esp_lower:
                    gramos = min(50 + (edad_dia * 3), 180)
                elif "codorniz" in esp_lower:
                    gramos = 30
                else:
                    gramos = min(80 + (edad_dia * 0.5), 125)
                consumo_lote += (vivas * (gramos / 1000))

            consumo_acumulado_total += consumo_lote
            consumo_por_especie[especie] = consumo_por_especie.get(especie, 0) + consumo_lote

    stock_actual = max(0, total_comprado - consumo_acumulado_total)
    return round(stock_actual, 2), round(consumo_acumulado_total, 2), consumo_por_especie

def calcular_autonomia(df_lotes, df_bajas, df_gastos, temp):
    stock_real, _, _ = obtener_estado_pienso(df_lotes, df_bajas, df_gastos)
    # Cálculo simplificado para autonomía diaria
    consumo_hoy = 5.0 
    if temp > 30: consumo_hoy *= 1.15
    autonomia = int(stock_real / consumo_hoy) if consumo_hoy > 0 else 0
    return autonomia, round(consumo_hoy, 2)

def get_clima_cartagena(api_key):
    return 18.5

# Variable de configuración para la IA
CONFIG_IA = {
    "modelo": "gemini-1.5-flash",
    "temperatura": 0.7
}