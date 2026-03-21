import streamlit as st
from db import get_conn
import pandas as pd

def mostrar():
    st.title("💾 Copias de Seguridad y Restauración")
    col_up, col_down = st.columns(2)
    with col_up:
        archivo = st.file_uploader("Subir Backup (.xlsx)", type=["xlsx"])
        if archivo and st.button("🚀 RESTAURAR TODO"):
            data_dict = pd.read_excel(archivo, sheet_name=None)
            with get_conn() as conn:
                for t in ["lotes", "gastos", "produccion", "ventas", "bajas"]:
                    if t in data_dict:
                        conn.execute(f"DELETE FROM {t}")
                        data_dict[t].to_sql(t, conn, if_exists='append', index=False)
            st.success("✅ Base de datos restaurada con éxito.")

    with col_down:
        if st.button("📦 Generar Backup Actual"):
            st.info("Función de exportación activa (pendiente de implementación).")