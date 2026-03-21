import os
import subprocess
import sys

# ============================
# 1. Carpetas del proyecto
# ============================
carpetas = [
    "vistas",
    "db",
    "utils",
    "assets"
]

for carpeta in carpetas:
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
        print(f"[+] Carpeta creada: {carpeta}")
    else:
        print(f"[i] Carpeta ya existe: {carpeta}")

# ============================
# 2. Archivos base
# ============================
archivos_base = {
    "main.py": "# Archivo principal de Streamlit\nprint('Reemplazar con main.py')\n",
    "requirements.txt": """streamlit==1.26.0
pandas==2.1.0
numpy==1.25.0
plotly==5.18.0
google-generativeai==0.1.0
requests==2.31.0
openpyxl==3.1.2
"""
}

for ruta, contenido in archivos_base.items():
    if not os.path.exists(ruta):
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f"[+] Archivo creado: {ruta}")
    else:
        print(f"[i] Archivo ya existe: {ruta}")

# ============================
# 3. Instalar dependencias
# ============================
try:
    print("[*] Instalando dependencias...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("[+] Dependencias instaladas correctamente.")
except Exception as e:
    print("[!] Error instalando dependencias:", e)

# ============================
# 4. Mensaje final
# ============================
print("\n¡Setup completado! Ahora coloca tus módulos en 'vistas/', 'db/' y 'utils/' según la estructura.")
print("Luego ejecuta: streamlit run main.py")