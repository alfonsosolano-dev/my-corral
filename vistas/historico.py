import streamlit as st
from utils.utils import CONFIG_IA
from db import get_conn

def mostrar():
    st.title("📜 Registros Históricos")
    tabla_sel = st.selectbox("Ver tabla:", ["lotes", "produccion", "gastos", "ventas", "bajas", "fotos"])
    df_h = cargar_datos(tabla_sel)
    st.dataframe(df_h, use_container_width=True)
    if not df_h.empty:
        id_borrar = st.number_input("ID del registro a eliminar", min_value=int(df_h['id'].min()))
        if st.button("🗑️ Eliminar Registro"):
            with get_conn() as conn:
                conn.execute(f"DELETE FROM {tabla_sel} WHERE id=?", (id_borrar,))
            st.success(f"ID {id_borrar} eliminado.")