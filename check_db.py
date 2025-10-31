# --- check_db.py ---
# Este codigo sirve para verificar la base de datos

import sqlite3

DB_FILE = "biblioteca.db"
print(f"Verificando el archivo '{DB_FILE}'...")

try:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Este comando le pide a SQLite que liste todas las tablas maestras
    print("Ejecutando consulta en 'sqlite_master'...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    
    tablas = cursor.fetchall()
    
    print("\n--- ¡VERIFICACIÓN EXITOSA! ---")
    print(f"Tablas encontradas en '{DB_FILE}':")
    
    # Imprime las tablas que encontró
    tablas_encontradas = [tabla[0] for tabla in tablas]
    print(tablas_encontradas)
    
    if 'socios' in tablas_encontradas and 'libros' in tablas_encontradas:
        print("\n¡CORRECTO! Las tablas 'libros' y 'socios' existen.")
    else:
        print("\n¡ERROR! Faltan tablas. 'setup_db.py' no funcionó bien.")

    conn.close()

except sqlite3.Error as e:
    print(f"\n--- ¡VERIFICACIÓN FALLIDA! ---")
    print(f"Error al leer la base de datos: {e}")