import streamlit as st
from db import get_conn
from datetime import datetime

def mostrar(df_lotes):
    st.title("💰 Registro de Salidas")
    with st.form("f_ventas"):
        tipo = st.radio("Tipo de Salida", ["Venta Cliente", "Consumo Propio"])
        l_id = st.selectbox("Lote de Origen", df_lotes['id'].tolist() if not df_lotes.empty else [])
        cliente = st.text_input("Cliente / Familia")
        concepto = st.text_input("Concepto (Ej: Huevos XL, Pollo Limpio)")
        c1, c2, c3 = st.columns(3)
        uni = c1.number_input("Unidades", 1)
        kg = c2.number_input("Kg (ilos_finale)", 0.0)
        imp = c3.number_input("Importe Total €", 0.0)
        if st.form_submit_button("✅ Registrar Salida"):
            with get_conn() as conn:
                conn.execute("INSERT INTO ventas (fecha, cliente, tipo_venta, concepto, cantidad, lote_id, ilos_finale, unidades) VALUES (?,?,?,?,?,?,?,?)",
                             (datetime.now().strftime("%d/%m/%Y"), cliente, tipo, concepto, imp, l_id, kg, uni))
            st.success("Salida registrada correctamente.")