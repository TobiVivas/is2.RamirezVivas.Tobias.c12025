import sqlite3
import os

DB_FILE = "biblioteca.db"

# Borra la base de datos vieja (si existe) para empezar de cero
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"Base de datos '{DB_FILE}' anterior eliminada.")

print(f"Creando nueva base de datos '{DB_FILE}'...")
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Crea la tabla de Libros 
print("Creando tabla 'libros'...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS libros (
    isbn TEXT PRIMARY KEY,
    titulo TEXT NOT NULL,
    disponible INTEGER NOT NULL
)
""")

# Crea la tabla de Socios 
print("Creando tabla 'socios'...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS socios (
    id TEXT PRIMARY KEY, 
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE, 
    multas_pendientes INTEGER NOT NULL
)
""")

print("Tablas creadas. Insertando datos iniciales...")

# Inserta los Libros 
libros_iniciales = [
    ("ISBN-001", "El Quijote", 1),
    ("ISBN-002", "1984", 0)
]
cursor.executemany("INSERT OR IGNORE INTO libros VALUES (?, ?, ?)", libros_iniciales)

# Inserta Socios 
socios_iniciales = [
    # (id, nombre, email, multas)
    ("Socio-1", "Ana", "ana@mail.com", 0),
    ("Socio-2", "Juan", "juan@mail.com", 1)
]
cursor.executemany("INSERT OR IGNORE INTO socios VALUES (?, ?, ?, ?)", socios_iniciales)

# Guarda los cambios y cerra
conn.commit()
conn.close()

print(f"¡Base de datos '{DB_FILE}' creada y lista!")