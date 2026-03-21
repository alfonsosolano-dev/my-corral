import streamlit as st
import plotly.express as px
from utils import calcular_autonomia

def mostrar(df_lotes, df_gastos, df_ventas, df_prod, df_bajas, temp):
    st.title(f"🏠 Panel de Control Maestro (Cartagena: {temp}°C)")

    # KPIs
    total_inv = df_gastos['cantidad'].sum() if not df_gastos.empty else 0
    caja_real = df_ventas[df_ventas['tipo_venta']=='Venta Cliente']['cantidad'].sum() if not df_ventas.empty else 0
    ahorro_casa = df_ventas[df_ventas['tipo_venta']=='Consumo Propio']['cantidad'].sum() if not df_ventas.empty else 0
    beneficio = (caja_real + ahorro_casa) - total_inv

    autonomia, consumo_dia = calcular_autonomia(df_lotes, df_bajas, df_gastos, temp)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Inversión Total", f"{total_inv:.2f} €")
    c2.metric("📈 Beneficio (Real+Casa)", f"{beneficio:.2f} €", delta=f"{caja_real:.2f} Caja")
    c3.metric("⚖️ Stock Pienso", f"{df_gastos['ilos_pienso'].sum() if not df_gastos.empty else 0:.1f} kg")
    c4.metric("⏳ Autonomía", f"{autonomia} días", delta="-Calor" if temp>30 else None)

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        if not df_prod.empty:
            fig_prod = px.area(df_prod.tail(30), x='fecha', y='huevos', title="Evolución Puesta (30d)", color_discrete_sequence=['gold'])
            st.plotly_chart(fig_prod, use_container_width=True)
    with col_b:
        if not df_lotes.empty:
            fig_pie = px.pie(df_lotes, values='cantidad', names='raza', title="Censo por Raza", hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)