import streamlit as st
from config import DB_PATH, API_GEMINI, API_AEMET
from db import inicializar_db, cargar_datos
from vistas import dashboard, salud_ia, crecimiento, produccion, ventas, gastos, bajas, navidad, backup, historico

# Inicializar DB
inicializar_db()

# Cargar datos
df_lotes = cargar_datos("lotes")
df_prod = cargar_datos("produccion")
df_gastos = cargar_datos("gastos")
df_ventas = cargar_datos("ventas")
df_bajas = cargar_datos("bajas")
df_fotos = cargar_datos("fotos")

# Sidebar
st.sidebar.title("🚜 CORRAL OMNI V95")
menu = st.sidebar.selectbox("MENÚ PRINCIPAL", [
    "🏠 Dashboard",
    "🩺 Salud IA & Visión",
    "📈 Crecimiento y Pesaje",
    "🥚 Producción Diaria",
    "💰 Ventas y Ahorro",
    "💸 Gastos y Pienso",
    "💀 Registro de Bajas",
    "🎄 Plan Navidad 2026",
    "🐣 Alta de Lotes",
    "💾 Gestión de Backup",
    "📜 Histórico Total"
])

# Rutas de vistas
vistas = {
    "🏠 Dashboard": lambda: dashboard.mostrar(df_lotes, df_prod, df_gastos, df_ventas, df_bajas, API_AEMET),
    "🩺 Salud IA & Visión": lambda: salud_ia.mostrar(df_lotes, API_GEMINI),
    "📈 Crecimiento y Pesaje": lambda: crecimiento.mostrar(df_lotes),
    "🥚 Producción Diaria": lambda: produccion.mostrar(df_lotes),
    "💰 Ventas y Ahorro": lambda: ventas.mostrar(df_lotes),
    "💸 Gastos y Pienso": lambda: gastos.mostrar(df_lotes),
    "💀 Registro de Bajas": lambda: bajas.mostrar(df_lotes),
    "🎄 Plan Navidad 2026": lambda: navidad.mostrar(df_lotes),
    "🐣 Alta de Lotes": lambda: crecimiento.alta_lotes(df_lotes),
    "💾 Gestión de Backup": lambda: backup.mostrar(),
    "📜 Histórico Total": lambda: historico.mostrar()
}

# Ejecutar vista seleccionada
vistas[menu]()