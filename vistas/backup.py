import streamlit as st
import pandas as pd
import io
from db.db import get_conn

def mostrar():
    st.title("💾 Copias de Seguridad y Restauración")
    
    col_up, col_down = st.columns(2)

    with col_up:
        st.subheader("🚀 Restaurar Datos")
        archivo = st.file_uploader("Subir Backup (.xlsx)", type=["xlsx"])
        if archivo and st.button("🚀 EJECUTAR RESTAURACIÓN"):
            try:
                data_dict = pd.read_excel(archivo, sheet_name=None)
                # Usamos una sola conexión para todo el proceso
                conn = get_conn()
                for t in ["lotes", "gastos", "produccion", "ventas", "bajas"]:
                    if t in data_dict:
                        # 'replace' es la clave: borra la tabla vieja y crea la nueva exacta al Excel
                        data_dict[t].to_sql(t, conn, if_exists='replace', index=False)
                conn.close()
                st.success("✅ ¡Restauración completada! Los datos ya están en la nube.")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Error crítico: {e}")

    with col_down:
        st.subheader("📦 Generar Backup")
        if st.button("📦 Crear Excel Actual"):
            try:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    for t in ["lotes", "gastos", "produccion", "ventas", "bajas"]:
                        try:
                            df = pd.read_sql(f"SELECT * FROM {t}", get_conn())
                            df.to_excel(writer, sheet_name=t, index=False)
                        except:
                            continue # Si una tabla no existe aún, la salta
                
                st.download_button(
                    label="⬇️ Descargar Backup",
                    data=output.getvalue(),
                    file_name="Backup_Corral_Omni.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Error al exportar: {e}")