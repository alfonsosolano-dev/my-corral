def obtener_estado_pienso(df_lotes, df_bajas, df_gastos):
    import pandas as pd
    from datetime import datetime
    
    if df_lotes.empty or df_gastos.empty:
        return 0, {}

    # 1. Total de kilos comprados (Histórico de entradas)
    total_comprado = df_gastos['ilos_pienso'].sum()
    
    # 2. Calcular consumo acumulado por especie
    consumo_acumulado_total = 0
    detalle_especies = {}

    for _, lote in df_lotes.iterrows():
        # Aves actuales
        bajas = df_bajas[df_bajas['lote'] == lote['id']]['cantidad'].sum() if not df_bajas.empty else 0
        vivas = lote['cantidad'] - bajas
        if vivas <= 0: continue

        # Cálculo de días y edad
        fecha_lote = pd.to_datetime(lote['fecha'])
        dias_en_corral = (datetime.now() - fecha_lote).days
        
        consumo_lote = 0
        especie = lote['especie']
        
        # Simulamos el crecimiento día a día para este lote
        for dia in range(dias_en_corral + 1):
            edad_ese_dia = lote['edad_inicial'] + dia
            
            # Curva de consumo (gramos/día)
            if "broiler" in especie.lower():
                gramos = min(50 + (edad_ese_dia * 3), 180)
            elif "codorniz" in especie.lower():
                gramos = 25 if edad_ese_dia < 20 else 35
            else: # Ponedoras
                gramos = min(80 + (edad_ese_dia * 0.5), 120)
            
            consumo_lote += (vivas * (gramos / 1000))

        consumo_acumulado_total += consumo_lote
        
        # Guardar por especie para el histórico
        if especie not in detalle_especies:
            detalle_especies[especie] = 0
        detalle_especies[especie] += consumo_lote

    # 3. Stock Real Actual
    stock_actual = max(0, total_comprado - consumo_acumulado_total)
    
    return round(stock_actual, 2), detalle_especies