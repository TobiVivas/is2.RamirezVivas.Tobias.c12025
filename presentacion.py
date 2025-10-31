# --- presentacion.py ---

# Se importa capa de negocio,datos y la configuracion para que corra correctamente el programa
from negocio.negocio import GestorBiblioteca
from datos.datos import BibliotecaDB
from configuracion import ConfiguracionSistema 

class AppTerminal:
    
    def __init__(self, gestor):
        """
        Recibe el gestor (DI) al ser creada.
        """
        self.gestor = gestor
        print("--- Sistema de Gestión de Biblioteca ---")

    def _mostrar_menu(self):
        """Muestra el menú principal de opciones."""
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Realizar un préstamo")
        print("2. Registrar una devolución")
        print("3. Agregar nuevo socio")
        print("4. Listar todos los socios") 
        print("5. Salir")                 

    def iniciar_app(self):
        """Mantiene la aplicación corriendo con un bucle principal."""
        while True:
            self._mostrar_menu()
            opcion = input("Seleccione una opción (1-5): ")

            if opcion == '1':
                self._ui_realizar_prestamo()
            elif opcion == '2':
                self._ui_registrar_devolucion()
            elif opcion == '3':
                self._ui_agregar_socio()
            elif opcion == '4': 
                self._ui_listar_socios()
            elif opcion == '5': 
                print("\nGracias por usar el sistema. ¡Adiós!")
                break
            else:
                print("\n[ERROR] Opción no válida. Por favor, intente de nuevo.")

    def _ui_realizar_prestamo(self):
        """Interfaz de usuario para la función de préstamo."""
        print("\n--- 1. Realizar Préstamo ---")
        isbn = input("Ingrese el ISBN del libro: ").strip()
        # Pide el ID del socio
        socio_id = input("Ingrese el ID del socio (ej: Socio-1): ").strip()

        # Validación de presentación
        if not isbn or not socio_id:
            print("\n[ERROR] El ISBN y el ID de Socio no pueden estar vacíos.")
            return

        try:
            # Llama a la capa de negocio con el socio_id
            mensaje_exito = self.gestor.realizar_prestamo(socio_id, isbn)
            print(f"\n[ÉXITO] {mensaje_exito}")

        except Exception as e:
            print(f"\n[ERROR DE NEGOCIO] {e}")
    def _ui_registrar_devolucion(self):
        """Interfaz de usuario para la función de devolución."""
        print("\n--- 2. Registrar Devolución ---")
        isbn = input("Ingrese el ISBN del libro a devolver: ").strip()

        if not isbn:
            print("\n[ERROR] El ISBN no puede estar vacío.")
            return

        try:
            mensaje_exito = self.gestor.registrar_devolucion(isbn)
            print(f"\n[ÉXITO] {mensaje_exito}")
        except Exception as e:
            print(f"\n[ERROR DE NEGOCIO] {e}")

    def _ui_agregar_socio(self):
        """Interfaz de usuario para agregar un nuevo socio."""
        print("\n--- 3. Agregar Nuevo Socio ---")
        # Pide los 3 campos para agregar un nuevo socio
        socio_id = input("Ingrese el nuevo ID para el socio (ej: Socio-3): ").strip()
        nombre = input("Ingrese el nombre completo: ").strip()
        email = input("Ingrese el email: ").strip()
        
        if not socio_id or not nombre or not email:
            print("\n[ERROR] El ID, el nombre y el email son obligatorios.")
            return

        try:
            mensaje_exito = self.gestor.agregar_socio(socio_id, nombre, email)
            print(f"\n[ÉXITO] {mensaje_exito}")
        except Exception as e:
            print(f"\n[ERROR DE NEGOCIO] {e}")
            

    def _ui_listar_socios(self):
        """
        Interfaz de usuario para listar todos los socios registrados.
        """
        print("\n--- 4. Lista de Socios Registrados ---")
        
        try:
            # Llama a la capa de negocio
            lista_socios = self.gestor.obtener_lista_socios()
            
            # Verifica si hay resultados
            if not lista_socios:
                print("\nNo hay socios registrados en el sistema.")
                return

            # Muestra los resultados en una tabla formateada
            print(f"\n{'ID':<10} | {'Nombre':<15} | {'Email':<25} | {'Multas':<10}")
            print("-" * 65)
            
            for socio in lista_socios:
                multas_str = "Sí" if socio["multas_pendientes"] else "No"
                
                # Muestra los datos usando las columnas correctas (id, nombre, email)
                print(f"{socio['id']:<10} | {socio['nombre']:<15} | {socio['email']:<25} | {multas_str:<10}")
        
        except Exception as e:
            print(f"\n[ERROR] No se pudo obtener la lista de socios: {e}")


# --- Inicializamos ---
if __name__ == "__main__":
    
    print("--- 1. Creando Dependencias ---")
    config_real = ConfiguracionSistema(archivo_config_path="config_prod.ini")
    db_real = BibliotecaDB(config=config_real)
    gestor_real = GestorBiblioteca(db=db_real, config=config_real)

    print("\n--- 2. Iniciando Aplicación ---")
    app = AppTerminal(gestor=gestor_real)
    app.iniciar_app()
