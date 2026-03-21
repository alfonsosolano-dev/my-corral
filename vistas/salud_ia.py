import streamlit as st
from db import get_conn
from datetime import datetime
import google.generativeai as genai

def mostrar(df_lotes, api_gemini):
    st.title("🩺 Análisis Veterinario por IA")
    if not api_gemini:
        st.warning("⚠️ Introduce la API Key de Gemini para activar la visión.")
        return

    lote_id = st.selectbox("Seleccionar Lote", df_lotes['id'].tolist() if not df_lotes.empty else [])
    img_input = st.file_uploader("Subir Foto de Aves", type=['jpg','jpeg','png'])
    if img_input:
        if st.button("🔍 Analizar Salud"):
            genai.configure(api_key=api_gemini)
            model = genai.GenerativeModel("gemini-1.5-flash")
            with st.spinner("Analizando..."):
                res = model.generate_content(["Analiza la salud de estas aves. Busca picaje, estado de plumas y vitalidad.",
                                             {"mime_type": "image/jpeg", "data": img_input.read()}])
                st.info(res.text)
                with get_conn() as conn:
                    conn.execute("INSERT INTO fotos (lote_id, fecha, imagen, nota_ia) VALUES (?,?,?,?)",
                                 (lote_id, datetime.now().strftime("%d/%m/%Y"), img_input.getvalue(), res.text))
                st.success("Diagnóstico guardado en el histórico.")