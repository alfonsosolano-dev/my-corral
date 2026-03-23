import pandas as pd
from datetime import datetime
from db.db import get_conn # Esta importación es segura ahora

def cargar_datos(tabla):
    try:
        with get_conn() as conn:
            return pd.read_sql(f"SELECT * FROM {tabla}", conn)
    except:
        return pd.DataFrame()

def obtener_estado_pienso(df_lotes, df_bajas, df_gastos):
    """Calcula el stock real restando el consumo acumulado por edad y especie"""
    if df_gastos.empty:
        return 0.0, 0.0, {}

    # 1. Total de kilos comprados históricamente
    total_comprado = df_gastos['ilos_pienso'].sum() if 'ilos_pienso' in df_gastos.columns else 0
    
    consumo_acumulado_total = 0
    consumo_por_especie = {}

    if not df_lotes.empty:
        for _, lote in df_lotes.iterrows():
            # Aves vivas
            bajas = df_bajas[df_bajas['lote'] == lote['id']]['cantidad'].sum() if not df_bajas.empty else 0
            vivas = lote['cantidad'] - bajas
            if vivas <= 0: continue

            # Cálculo de días (Desde fecha de registro hasta hoy)
            try:
                # Aseguramos que la fecha esté en formato datetime
                fecha_lote = pd.to_datetime(lote['fecha'])
                dias_totales = (datetime.now() - fecha_lote).days
                if dias_totales < 0: dias_totales = 0
            except:
                dias_totales = 0
            
            especie = str(lote['especie'])
            consumo_lote = 0

            # Calculamos el consumo día a día (crecimiento acumulado)
            for d in range(dias_totales + 1):
                edad_dia = lote['edad_inicial'] + d
                
                # Curva de gramos/día (Aumenta según crecen)
                esp_lower = especie.lower()
                if "pollo" in esp_lower or "broiler" in esp_lower:
                    gramos = min(50 + (edad_dia * 3), 180)
                elif "codorniz" in esp_lower:
                    gramos = 25 if edad_dia < 20 else 35
                else: # Gallinas ponedoras
                    gramos = min(80 + (edad_dia * 0.5), 125)
                
                consumo_lote += (vivas * (gramos / 1000))

            consumo_acumulado_total += consumo_lote
            
            # Guardamos el desglose por especie
            if especie not in consumo_por_especie:
                consumo_por_especie[especie] = 0
            consumo_por_especie[especie] += consumo_lote

    # 2. Stock Real Actual (Entradas - Salidas consumidas)
    stock_actual = max(0, total_comprado - consumo_acumulado_total)
    
    return round(stock_actual, 2), round(consumo_acumulado_total, 2), consumo_por_especie

def calcular_autonomia(df_lotes, df_bajas, df_gastos, temp):
    # Cambia el nombre aquí también:
    stock_real, _, _ = obtener_estado_pienso(df_lotes, df_bajas, df_gastos) 
    ...
    
    consumo_hoy = 0
    if not df_lotes.empty:
        for _, lote in df_lotes.iterrows():
            bajas = df_bajas[df_bajas['lote'] == lote['id']]['cantidad'].sum() if not df_bajas.empty else 0
            vivas = lote['cantidad'] - bajas
            if vivas <= 0: continue

            dias_hoy = (datetime.now() - pd.to_datetime(lote['fecha'])).days
            edad_hoy = lote['edad_inicial'] + dias_hoy
            
            esp_lower = str(lote['especie']).lower()
            if "pollo" in esp_lower or "broiler" in esp_lower:
                gr = min(50 + (edad_hoy * 3), 180)
            elif "codorniz" in esp_lower:
                gr = 35
            else:
                gr = min(80 + (edad_hoy * 0.5), 125)
            
            consumo_hoy += (vivas * (gr / 1000))

    # Ajuste por temperatura (Cartagena)
    if temp > 30: consumo_hoy *= 1.15
    elif temp < 10: consumo_hoy *= 1.10

    autonomia = int(stock_real / consumo_hoy) if consumo_hoy > 0 else 0
    return autonomia, round(consumo_hoy, 2)

def get_clima_cartagena(api_key):
    """Función simplificada para obtener temperatura"""
    # Por ahora devolvemos un valor fijo o lógica de API si la tienes configurada
    return 18.5 # Valor por defecto si no hay API activa

# Variable de configuración para la IA
CONFIG_IA = {
    "modelo": "gemini-1.5-flash",
    "temperatura": 0.7
}