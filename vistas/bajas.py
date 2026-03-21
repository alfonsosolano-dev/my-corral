import streamlit as st
from db.db import get_conn
from datetime import datetime

def mostrar(df_lotes):
    st.title("💀 Registro de Bajas")
    with st.form("f_bajas"):
        l_id = st.selectbox("Lote", df_lotes['id'].tolist() if not df_lotes.empty else [])
        cant = st.number_input("Cantidad de bajas", 1)
        mot = st.text_input("Motivo")
        if st.form_submit_button("Registrar Baja"):
            with get_conn() as conn:
                conn.execute("INSERT INTO bajas (fecha, lote, cantidad, motivo) VALUES (?,?,?,?)",
                             (datetime.now().strftime("%d/%m/%Y"), l_id, int(cant), mot))
            st.success("Baja registrada correctamente.")