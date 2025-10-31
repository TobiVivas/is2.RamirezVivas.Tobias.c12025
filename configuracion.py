# --- configuracion.py ---

class ConfiguracionSistema:
    """
    Clase simple que carga datos de configuración.
    ( una clase normal para DI).
    """
    def __init__(self, archivo_config_path: str):
        # (Aca se podria leer un archivo .ini o .env)
        print(f"Cargando configuración desde {archivo_config_path}...")
        
        # Simulamos los datos leídos
        self.config_data = {
            # ¡La clave que usa la Capa de Datos ahora apunta a nuestro archivo SQLite!
            "url_base_datos": "biblioteca.db", 
            "dias_max_prestamo": 15,
            "multa_por_dia": 1.50
        }

    def get_config(self, clave):
        return self.config_data.get(clave)