import streamlit as st
from db import get_conn
from datetime import datetime

def mostrar():
    st.title("💸 Registro de Gastos")
    with st.form("f_gastos"):
        cat = st.selectbox("Categoría", ["Pienso Gallinas", "Pienso Pollos", "Medicina", "Infraestructura", "Compra Aves"])
        con = st.text_input("Concepto Detallado")
        c1, c2 = st.columns(2)
        imp = c1.number_input("Importe €", 0.0)
        kg_p = c2.number_input("Kg Comprados (ilos_pienso)", 0.0)
        if st.form_submit_button("💾 Guardar Gasto"):
            with get_conn() as conn:
                conn.execute("INSERT INTO gastos (fecha, categoria, concepto, cantidad, ilos_pienso) VALUES (?,?,?,?,?)",
                             (datetime.now().strftime("%d/%m/%Y"), cat, con, imp, kg_p))
            st.success("Gasto registrado correctamente.")