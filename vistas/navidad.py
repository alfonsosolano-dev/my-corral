import streamlit as st
from datetime import datetime, timedelta
from utils.utils import CONFIG_IA
import pandas as pd

def mostrar():
    st.title("🎄 Planificador de Campaña Navideña")
    f_cena = datetime(2026, 12, 20)
    st.write(f"Aves listas para el **{f_cena.strftime('%d/%m/%Y')}**")
    data_nav = []
    for raza, info in CONFIG_IA.items():
        if "madurez" in info:
            f_compra = f_cena - timedelta(days=info['madurez'])
            data_nav.append({"Raza": raza, "Días Crecimiento": info['madurez'], "Fecha Compra": f_compra.strftime('%d/%m/%Y')})
    st.table(pd.DataFrame(data_nav))
    st.info("💡 Consejo IA: Compra 1 semana antes de la fecha indicada para margen de peso.")