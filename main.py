import streamlit as st
from db.db import inicializar_db
from utils.utils import cargar_datos, get_clima_cartagena
from vistas import (dashboard, alta_lotes, salud_ia, produccion, ventas, gastos,
                    bajas, navidad, backup, historico)

# Configuración de página
st.set_page_config(page_title="Corral Omni V95", layout="wide")
inicializar_db()

try:
    df_lotes = cargar_datos("lotes")
    df_gastos = cargar_datos("gastos")
    df_ventas = cargar_datos("ventas")
    df_prod = cargar_datos("produccion")
    df_bajas = cargar_datos("bajas")
except:
    df_lotes = df_gastos = df_ventas = df_prod = df_bajas = None

# Sidebar
st.sidebar.title("🚜 CORRAL OMNI V95")
with st.sidebar.expander("🔑 Configuración API"):
    api_gemini = st.text_input("Gemini API Key", type="password")
    api_aemet = st.text_input("AEMET API Key", type="password")

menu = st.sidebar.selectbox("MENÚ PRINCIPAL", 
    ["🏠 Dashboard", "🩺 Salud IA & Visión", "📈 Crecimiento y Pesaje", "🥚 Producción Diaria", 
     "💰 Ventas y Ahorro", "💸 Gastos y Pienso", "💀 Registro de Bajas", "🎄 Plan Navidad 2026", 
     "🐣 Alta de Lotes", "💾 Gestión de Backup", "📜 Histórico Total"])

# Obtener temperatura
temp_cartagena = get_clima_cartagena(api_aemet)

# Llamadas a vistas
if menu=="🏠 Dashboard": dashboard.mostrar(df_lotes, df_gastos, df_ventas, df_prod, df_bajas, temp_cartagena)
elif menu=="🐣 Alta de Lotes": alta_lotes.mostrar()
elif menu=="🩺 Salud IA & Visión": salud_ia.mostrar(df_lotes, api_gemini)
elif menu=="🥚 Producción Diaria": produccion.mostrar(df_lotes)
elif menu=="💰 Ventas y Ahorro": ventas.mostrar(df_lotes)
elif menu=="💸 Gastos y Pienso": gastos.mostrar()
elif menu=="💀 Registro de Bajas": bajas.mostrar(df_lotes)
elif menu=="🎄 Plan Navidad 2026": navidad.mostrar()
elif menu=="💾 Gestión de Backup": backup.mostrar()
elif menu=="📜 Histórico Total": historico.mostrar()