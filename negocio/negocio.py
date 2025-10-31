# ¡IMPORTA LA CAPA DE DATOS!
from datos.datos import BibliotecaDB 

class GestorBiblioteca:
    # Método para inicializar
    def __init__(self, db, config):
        self.db = db
        self.config = config
        print(f"[Negocio] Gestor inicializado.")
    # Método para calcular multa
    def calcular_multa(self, dias_retraso):
        multa_base = self.config.get_config("multa_por_dia")
        return multa_base * dias_retraso
    # Método para calcular dias de devolucion
    def calcular_dias_devolucion(self):
        dias = self.config.get_config("dias_max_prestamo")
        print(f"[Negocio] El préstamo dura {dias} días.")
        return dias

    # Método para realizar prestamo
    def realizar_prestamo(self, socio_id, isbn):
        print(f"[Negocio] Recibida orden de préstamo para {socio_id} y {isbn}")

        #  PIDE los datos a la capa de datos
        socio = self.db.get_socio_por_id(socio_id) # Busca por ID
        libro = self.db.get_libro_por_isbn(isbn)

        # REGLAS DE NEGOCIO 
        if not socio:
            raise ValueError(f"Préstamo RECHAZADO: El socio {socio_id} no existe.") # Mensaje actualizado
        
        if not libro:
            raise ValueError(f"Préstamo RECHAZADO: El libro {isbn} no se encuentra.")
        
        if socio["multas_pendientes"]:
            raise ValueError(f"Préstamo RECHAZADO: El socio {socio['nombre']} tiene multas pendientes.")
        
        if not libro["disponible"]:
             raise ValueError(f"Préstamo RECHAZADO: El libro '{libro['titulo']}' ya está prestado.")
        
        # ORDENA guardar a la capa de datos
        self.db.guardar_prestamo(socio_id, isbn) # Pasa el ID
        
        return f"Préstamo de '{libro['titulo']}' a '{socio['nombre']}' registrado exitosamente."

    # Método para registrar devolucion
    def registrar_devolucion(self, isbn):
        print(f"[Negocio] Recibida orden de devolución para {isbn}")
        
        libro = self.db.get_libro_por_isbn(isbn)
        
        # REGLAS DE NEGOCIO
        if not libro:
            raise ValueError(f"Devolución RECHAZADA: El libro {isbn} no existe.")
        
        if libro["disponible"]:
            raise ValueError(f"Devolución RECHAZADA: El libro '{libro['titulo']}' ya figura como disponible.")

        # Llama a la capa de datos
        self.db.registrar_devolucion_db(isbn)
        return f"Devolución de '{libro['titulo']}' ({isbn}) registrada. ¡Gracias!"

    # Método para agregar socio
    def agregar_socio(self, socio_id, nombre, email):
        print(f"[Negocio] Recibida orden de agregar socio {nombre} con ID {socio_id}")

        #  REGLAS DE NEGOCIO
        if not socio_id:
             raise ValueError("Registro RECHAZADO: El ID del socio no puede estar vacío.")
        
        if not email or "@" not in email:
            raise ValueError("Registro RECHAZADO: El email proporcionado no es válido.")

        try:
            #  LLAMA A LA CAPA DE DATOS
            self.db.guardar_socio(socio_id, nombre, email)
            
            #  Devuelve éxito
            return f"Socio '{nombre}' ({socio_id}) creado con éxito."
        
        except ValueError as e:
            #  Captura errores de la BD (ej: ID o email duplicado)
            raise e
        
    def obtener_lista_socios(self):
        print("[Negocio] Solicitando lista de socios a la capa de datos.")
        try:
            # Obtiene la lista completa de socios.
            # Llama al nuevo método de la capa de datos
            lista_de_socios = self.db.get_todos_los_socios()
            return lista_de_socios
        except Exception as e:
            # Maneja cualquier error inesperado de la BD
            raise ValueError(f"No se pudo obtener la lista de socios: {e}")