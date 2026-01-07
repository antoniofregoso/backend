import logging
import sys
from settings import settings

# Configuración del formato de logs
# Ejemplo: 2023-10-27 10:00:00,123 - INFO - [main.py:15] - Mensaje de prueba
LOG_FORMAT = "%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"

def configure_logging():
    """Configura el logging global de la aplicación."""
    
    # Obtener el nivel de log desde settings (ej. "DEBUG", "INFO")
    numeric_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    # Configuración básica
    logging.basicConfig(
        level=numeric_level,
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout)  # Enviar logs a la consola (stdout)
        ]
    )
    
    # Ajustar logs de librerías ruidosas
    logging.getLogger("multipart").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING) # Menos ruido de requests http normales

    # Crear logger raíz para pruebas
    logger = logging.getLogger("api")
    logger.info(f"Logging configurado. Nivel: {settings.LOG_LEVEL}")

# Instancia lista para importar si se necesita un logger rápido,
# aunque se recomienda usar logging.getLogger(__name__) en cada archivo.
def get_logger(name: str):
    return logging.getLogger(name)
