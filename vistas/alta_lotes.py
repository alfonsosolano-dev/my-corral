import streamlit as st
**from db.db import get_conn**
from utils.utils import CONFIG_IA
from datetime import datetime

def mostrar():
    st.title("🐣 Registro de Nuevas Aves")
    with st.form("f_alta"):
        esp = st.selectbox("Especie", ["Gallina", "Pollo", "Codorniz", "Pato", "Pavo"])
        rz = st.selectbox("Raza", list(CONFIG_IA.keys()) + ["Otras"])
        c1, c2, c3 = st.columns(3)
        cant = c1.number_input("Cantidad inicial", 1)
        ed = c2.number_input("Edad al entrar (Días)", 0)
        pr = c3.number_input("Precio por unidad €", 0.0)
        f_alta = st.date_input("Fecha de entrada")
        if st.form_submit_button("🐣 Dar de Alta"):
            with get_conn() as conn:
                conn.execute("INSERT INTO lotes (fecha, especie, raza, cantidad, edad_inicial, precio_ud, estado) VALUES (?,?,?,?,?,?,'Activo')",
                             (f_alta.strftime("%d/%m/%Y"), esp, rz, int(cant), int(ed), pr))
            st.success("Lote registrado correctamente.")