import streamlit as st
from db import get_conn
from datetime import datetime

def mostrar(df_lotes):
    st.title("🥚 Registro de Producción Diaria")
    with st.form("f_produccion"):
        l_id = st.selectbox("Seleccionar Lote", df_lotes['id'].tolist() if not df_lotes.empty else [])
        h = st.number_input("Huevos recogidos", 1)
        if st.form_submit_button("💾 Guardar Producción"):
            with get_conn() as conn:
                conn.execute("INSERT INTO produccion (fecha, lote, huevos) VALUES (?,?,?)",
                             (datetime.now().strftime("%d/%m/%Y"), l_id, h))
            st.success("Producción guardada.")