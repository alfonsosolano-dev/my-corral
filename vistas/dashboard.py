import streamlit as st
import plotly.express as px
# Importamos EXACTAMENTE los mismos nombres que pusimos en utils.py
from utils.utils import calcular_autonomia, obtener_estado_pienso

def mostrar(df_lotes, df_gastos, df_ventas, df_prod, df_bajas, temp):
    st.title(f"🏠 Panel de Control Maestro (Cartagena: {temp}°C)")

    # 1. CÁLCULOS DE DINERO
    total_inv = df_gastos['cantidad'].sum() if not df_gastos.empty else 0
    caja_real = df_ventas[df_ventas['tipo_venta']=='Venta Cliente']['cantidad'].sum() if not df_ventas.empty else 0
    ahorro_casa = df_ventas[df_ventas['tipo_venta']=='Consumo Propio']['cantidad'].sum() if not df_ventas.empty else 0
    beneficio = (caja_real + ahorro_casa) - total_inv

    # 2. CÁLCULOS DE PIENSO DINÁMICO
    # Llamamos a la función que acabamos de crear en utils.py
    stock_real, desglose = obtener_estado_pienso(df_lotes, df_bajas, df_gastos)
    autonomia, consumo_dia = calcular_autonomia(df_lotes, df_bajas, df_gastos, temp)

    # 3. FILA DE INDICADORES (KPIs)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Inversión Total", f"{total_inv:.2f} €")
    c2.metric("📈 Beneficio", f"{beneficio:.2f} €", delta=f"{caja_real:.2f} Caja")
    c3.metric("⚖️ Stock Almacén", f"{stock_real:.1f} kg", 
              delta=f"-{round(sum(desglose.values()), 1)} comidos", delta_color="inverse")
    c4.metric("⏳ Autonomía", f"{autonomia} días", delta=f"{consumo_dia:.2f} kg/día", delta_color="off")

    st.divider()

    # 4. GRÁFICOS
    col_a, col_b = st.columns(2)
    with col_a:
        if not df_prod.empty:
            fig_prod = px.area(df_prod.tail(30), x='fecha', y='huevos', title="Evolución Puesta (30d)", color_discrete_sequence=['gold'])
            st.plotly_chart(fig_prod, use_container_width=True)
    with col_b:
        if not df_lotes.empty:
            fig_pie = px.pie(df_lotes, values='cantidad', names='especie', title="Censo por Especie", hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)

    # 5. HISTÓRICO POR ESPECIE
    st.subheader("📉 Consumo Histórico por Especie")
    if desglose:
        cols_esp = st.columns(len(desglose))
        for i, (especie, kilos) in enumerate(desglose.items()):
            cols_esp[i].metric(label=f"Consumido: {especie}", value=f"{round(kilos, 1)} kg")