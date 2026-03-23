import sqlite3

# Definimos la ruta aquí para romper el ciclo de importación
DB_PATH = "corral_maestro_pro.db"

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def inicializar_db():
    with get_conn() as conn:
        # Tabla de Gastos con la columna clave: ilos_pienso
        conn.execute("""
            CREATE TABLE IF NOT EXISTS gastos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                categoria TEXT,
                concepto TEXT,
                cantidad REAL,
                ilos_pienso REAL
            )
        """)
        # ... resto de tablas (lotes, bajas, etc.)
        conn.commit()
        
        # 2. Tabla de Lotes (El origen de todo)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS lotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                especie TEXT,
                raza TEXT,
                cantidad INTEGER,
                edad_inicial INTEGER,
                estado TEXT DEFAULT 'Activo'
            )
        """)

        # 3. Tabla de Bajas (Para restar del censo)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bajas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                lote INTEGER,
                cantidad INTEGER,
                motivo TEXT
            )
        """)

        # 4. Tabla de Producción (Huevos)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS produccion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                lote INTEGER,
                huevos INTEGER
            )
        """)

        # 5. Tabla de Ventas y Consumo Propio
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                producto TEXT,
                cantidad REAL,
                precio_total REAL,
                tipo_venta TEXT
            )
        """)
        
        conn.commit()