import pandas as pd
from datetime import datetime

def obtener_inventario_pienso(df_lotes, df_bajas, df_gastos):
    if df_gastos.empty:
        return 0.0, 0.0, {}

    # 1. Total de kilos comprados históricamente
    total_comprado = df_gastos['ilos_pienso'].sum()
    
    consumo_acumulado_total = 0
    consumo_por_especie = {}

    if not df_lotes.empty:
        for _, lote in df_lotes.iterrows():
            # Aves vivas
            bajas = df_bajas[df_bajas['lote'] == lote['id']]['cantidad'].sum() if not df_bajas.empty else 0
            vivas = lote['cantidad'] - bajas
            if vivas <= 0: continue

            # Días que lleva el lote (desde su fecha de registro hasta hoy)
            fecha_lote = pd.to_datetime(lote['fecha'])
            dias_totales = (datetime.now() - fecha_lote).days
            
            especie = lote['especie']
            consumo_lote = 0

            # Calculamos el consumo día a día (crecimiento)
            for d in range(dias_totales + 1):
                edad_dia = lote['edad_inicial'] + d
                
                # Curva de gramos/día
                if "pollo" in especie.lower() or "broiler" in especie.lower():
                    # Crecimiento rápido: de 50g a 180g
                    gramos = min(50 + (edad_dia * 3), 180)
                elif "codorniz" in especie.lower():
                    gramos = 25 if edad_dia < 20 else 35
                else: # Gallinas ponedoras
                    gramos = min(80 + (edad_dia * 0.5), 125)
                
                consumo_lote += (vivas * (gramos / 1000))

            consumo_acumulado_total += consumo_lote
            
            # Guardamos el desglose
            if especie not in consumo_por_especie:
                consumo_por_especie[especie] = 0
            consumo_por_especie[especie] += consumo_lote

    # 2. Stock Real (Entradas - Salidas)
    stock_actual = max(0, total_comprado - consumo_acumulado_total)
    
    return round(stock_actual, 2), round(consumo_acumulado_total, 2), consumo_por_especie