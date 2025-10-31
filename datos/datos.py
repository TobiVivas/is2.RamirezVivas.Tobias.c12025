import sqlite3

class BibliotecaDB:
    # Método para inicializar
    def __init__(self, config):
        self.db_name = config.get_config("url_base_datos")
        if not self.db_name:
            raise ValueError("Error de Configuración: 'url_base_datos' no encontrada.")
        print(f"[Datos] Capa de Datos conectada a: {self.db_name}")
    # Método para conectarse a la base de datos
    def _get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    # Método para obtener libro por el codigo ISBN
    def get_libro_por_isbn(self, isbn):
        print(f"[Datos] Consultando BD SQLite por libro: {isbn}")
        conn = self._get_connection()
        cursor = conn.execute("SELECT * FROM libros WHERE isbn = ?", (isbn,))
        libro = cursor.fetchone()
        conn.close()
        return libro

    # Método para obtener el socio por id
    def get_socio_por_id(self, socio_id):
        print(f"[Datos] Consultando BD SQLite por socio: {socio_id}")
        conn = self._get_connection()
        cursor = conn.execute("SELECT * FROM socios WHERE id = ?", (socio_id,))
        socio = cursor.fetchone()
        conn.close()
        return socio
    # Método para guardar los prestamos 
    def guardar_prestamo(self, socio_id, isbn):
        """Actualiza el estado del libro a 'No disponible' (0)."""
        print(f"[Datos] Actualizando BD SQLite: Libro {isbn} -> No disponible")
        conn = self._get_connection()
        conn.execute("UPDATE libros SET disponible = 0 WHERE isbn = ?", (isbn,))
        conn.commit()
        conn.close()
        return True
    
    # Este Método registra devoluciones
    def registrar_devolucion_db(self, isbn):
        """Actualiza el estado del libro a 'Disponible' (1)."""
        print(f"[Datos] Actualizando BD SQLite: Libro {isbn} -> Disponible")
        conn = self._get_connection()
        conn.execute("UPDATE libros SET disponible = 1 WHERE isbn = ?", (isbn,))
        conn.commit()
        conn.close()
        return True
    
    # Método guardar socio
    def guardar_socio(self, socio_id, nombre, email):
        print(f"[Datos] Guardando nuevo socio en BD SQLite: {socio_id}")
        conn = self._get_connection()
        try:
            # El nuevo socio empieza sin multas (0)
            conn.execute(
                "INSERT INTO socios (id, nombre, email, multas_pendientes) VALUES (?, ?, ?, 0)",
                (socio_id, nombre, email)
            )
            conn.commit()
        except sqlite3.IntegrityError as e:
            # Fallará si el ID o el EMAIL ya existen
            conn.close()
            raise ValueError(f"No se pudo guardar: El ID '{socio_id}' o el email '{email}' ya existen.") from e
        conn.close()
        return True
    
    def get_todos_los_socios(self):
        """
        Recupera todos los socios de la base de datos.
        """
        print("[Datos] Consultando BD SQLite por TODOS los socios")
        conn = self._get_connection()
        # Ejecuta la consulta para obtener todos los socios
        cursor = conn.execute("SELECT * FROM socios ORDER BY nombre ASC")
        socios = cursor.fetchall()
        conn.close()
        # Devuelve una lista de objetos (similares a diccionarios)
        return socios
