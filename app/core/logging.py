import logging
import sys
import os
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler
from app.core.config import settings

# Crear directorio de logs si no existe
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Nombre del archivo de log con la fecha actual
log_file = log_dir / f"app_{datetime.now().strftime('%Y-%m-%d')}.log"

# Configuración del formato de los logs
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    "%Y-%m-%d %H:%M:%S"
)

# Handler para la consola
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# Handler para el archivo de log con rotación (10MB por archivo, máximo 5 archivos)
file_handler = RotatingFileHandler(
    log_file, maxBytes=10 * 1024 * 1024, backupCount=5
)
file_handler.setFormatter(formatter)

# Configuración del nivel de log según el entorno
def get_log_level():
    """Determinar el nivel de log según el entorno"""
    env = settings.ENVIRONMENT.lower()
    if env == "production":
        return logging.WARNING
    elif env == "testing":
        return logging.DEBUG
    else:  # development
        return logging.INFO


# Función para obtener un logger configurado para un módulo específico
def get_logger(name: str) -> logging.Logger:
    """
    Obtener un logger configurado para un módulo específico
    
    Args:
        name: Nombre del módulo (normalmente se usa __name__)
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Evitar duplicación de handlers
    if not logger.handlers:
        logger.setLevel(get_log_level())
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.propagate = False
    
    return logger 