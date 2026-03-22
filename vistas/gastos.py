import streamlit as st
from db.db import get_conn
from datetime import datetime

def mostrar():
    st.title("💸 Registro de Gastos")
    
    with st.form("f_gastos", clear_on_submit=True): # clear_on_submit limpia el formulario al terminar
        cat = st.selectbox("Categoría", ["Pienso Gallinas", "Pienso Pollos", "Medicina", "Infraestructura", "Compra Aves"])
        con = st.text_input("Concepto Detallado (ej: Saco 25kg Puesta)")
        
        c1, c2 = st.columns(2)
        imp = c1.number_input("Importe €", min_value=0.0, step=0.5)
        kg_p = c2.number_input("Kg Comprados (Pienso)", min_value=0.0, step=1.0)
        
        # Fecha en formato estándar ISO para que Python y SQL se entiendan siempre
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")

        if st.form_submit_button("💾 Guardar Gasto"):
            if imp > 0 or kg_p > 0:
                with get_conn() as conn:
                    conn.execute(
                        "INSERT INTO gastos (fecha, categoria, concepto, cantidad, ilos_pienso) VALUES (?,?,?,?,?)",
                        (fecha_hoy, cat, con, imp, kg_p)
                    )
                    conn.commit()
                st.success(f"✅ Gasto de {cat} registrado correctamente.")
            else:
                st.warning("⚠️ Por favor, introduce un importe o cantidad de kilos.")