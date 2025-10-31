# --- tests/test_negocio.py ---

import unittest
import sys
import os

# --- Hack de sys.path ---
# Esto es necesario para que el test pueda "ver" las carpetas 'negocio', 'datos', etc.
# Sube dos niveles (desde tests/test_negocio.py hasta la raíz del proyecto)
script_dir = os.path.dirname(__file__)
proyecto_raiz = os.path.dirname(script_dir)
sys.path.insert(0, proyecto_raiz)


from negocio.negocio import GestorBiblioteca

# -----------------------------------------------------
# Creamos Simuladores o tambien llamados Mocks
# -----------------------------------------------------

class MockBibliotecaDB:
    """
    Un simulador de la Capa de Datos.
    No se conecta a SQLite. Solo devuelve lo que le decimos.
    """
    def __init__(self):
        self.socio_a_devolver = None
        self.libro_a_devolver = None
        self.prestamo_guardado = False
        self.devolucion_guardada = False 

    def get_socio_por_id(self, socio_id):
        print(f"[MockDB] Buscando socio {socio_id}...")
        return self.socio_a_devolver

    def get_libro_por_isbn(self, isbn):
        print(f"[MockDB] Buscando libro {isbn}...")
        return self.libro_a_devolver

    def guardar_prestamo(self, socio_id, isbn):
        print("[MockDB] Guardando préstamo...")
        self.prestamo_guardado = True
        return True

    # Implementamos el mock para el test de devolución
    def registrar_devolucion_db(self, isbn): 
        print(f"[MockDB] Registrando devolución para {isbn}...")
        self.devolucion_guardada = True
        return True
        
    def guardar_socio(self, socio_id, nombre, email): pass
    def get_todos_los_socios(self): pass

class MockConfig:
    """Un simulador de la Configuración."""
    def get_config(self, clave):
        if clave == "dias_max_prestamo":
            return 15
        if clave == "multa_por_dia":
            return 1.50
        return None

# -----------------------------------------------------
# Creamos la Clase de Prueba
# -----------------------------------------------------

class TestGestorBiblioteca(unittest.TestCase):
    """
    Contiene todas las pruebas para la clase GestorBiblioteca.
    """

    def setUp(self):
        """
        Este método se ejecuta ANTES de CADA prueba (test_).
        Es perfecto para "resetear" el entorno.
        """
        # Creamos instancias frescas de nuestros Mocks
        self.mock_db = MockBibliotecaDB()
        self.mock_config = MockConfig()
        
        # Inyectamos los mocks en el Gestor
        self.gestor = GestorBiblioteca(db=self.mock_db, config=self.mock_config)

    # Pruebas existentes para 'realizar_prestamo'

    def test_realizar_prestamo_exitoso(self):
        print("\n--- Probando: Préstamo Exitoso ---")
        
        # Preparación 
        self.mock_db.socio_a_devolver = {"id": "Socio-1", "nombre": "Ana", "multas_pendientes": 0}
        self.mock_db.libro_a_devolver = {"isbn": "ISBN-001", "titulo": "El Quijote", "disponible": 1}

        # Acción (Act)
        mensaje = self.gestor.realizar_prestamo("Socio-1", "ISBN-001")

        # Verificación (Assert)
        self.assertEqual(mensaje, "Préstamo de 'El Quijote' a 'Ana' registrado exitosamente.")
        self.assertTrue(self.mock_db.prestamo_guardado) 

    def test_realizar_prestamo_socio_con_multas(self):
        print("\n--- Probando: Préstamo Rechazado (Socio con Multas) ---")
        
        # Preparación 
        self.mock_db.socio_a_devolver = {"id": "Socio-2", "nombre": "Juan", "multas_pendientes": 1}
        self.mock_db.libro_a_devolver = {"isbn": "ISBN-001", "titulo": "El Quijote", "disponible": 1}

        # Acción y Verificación (Act & Assert)
        with self.assertRaises(ValueError) as contexto:
            self.gestor.realizar_prestamo("Socio-2", "ISBN-001")

        self.assertEqual(
            str(contexto.exception),
            "Préstamo RECHAZADO: El socio Juan tiene multas pendientes."
        )
        self.assertFalse(self.mock_db.prestamo_guardado)

    def test_realizar_prestamo_libro_no_disponible(self):
        print("\n--- Probando: Préstamo Rechazado (Libro no disponible) ---")
        
        # Preparación
        self.mock_db.socio_a_devolver = {"id": "Socio-1", "nombre": "Ana", "multas_pendientes": 0}
        self.mock_db.libro_a_devolver = {"isbn": "ISBN-002", "titulo": "1984", "disponible": 0}

        # Acción y Verificación
        with self.assertRaises(ValueError) as contexto:
            self.gestor.realizar_prestamo("Socio-1", "ISBN-002")

        self.assertEqual(
            str(contexto.exception),
            "Préstamo RECHAZADO: El libro '1984' ya está prestado."
        )
        self.assertFalse(self.mock_db.prestamo_guardado)

    #  Pruebas simples para "libros a devolver"

    def test_registrar_devolucion_exitosa(self):
        print("\n--- Probando: Devolución Exitosa ---")
        
        # Preparación: Simulamos un libro que SÍ está prestado (disponible: 0)
        self.mock_db.libro_a_devolver = {"isbn": "ISBN-002", "titulo": "1984", "disponible": 0}

        # Acción
        mensaje = self.gestor.registrar_devolucion("ISBN-002")

        # Verificación
        self.assertEqual(mensaje, "Devolución de '1984' (ISBN-002) registrada. ¡Gracias!")
        self.assertTrue(self.mock_db.devolucion_guardada) # Verifica que se llamó a la BD

    def test_registrar_devolucion_libro_ya_disponible(self):
        print("\n--- Probando: Devolución Rechazada (Libro no estaba prestado) ---")
        
        # Preparación: Simulamos un libro que NO está prestado (disponible: 1)
        self.mock_db.libro_a_devolver = {"isbn": "ISBN-001", "titulo": "El Quijote", "disponible": 1}

        # Acción y Verificación
        with self.assertRaises(ValueError) as contexto:
            self.gestor.registrar_devolucion("ISBN-001")

        # Verifica el mensaje de error
        self.assertEqual(
            str(contexto.exception),
            "Devolución RECHAZADA: El libro 'El Quijote' ya figura como disponible."
        )
        # Verifica que NO se llamó a la BD para guardar
        self.assertFalse(self.mock_db.devolucion_guardada)


# Ejecuta las pruebas (solo si se ejecuta este archivo directamente)
if __name__ == "__main__":
    unittest.main()
