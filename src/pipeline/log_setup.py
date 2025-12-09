"""
Módulo de Log
----------------
Fecha: 2025-12-09
Descripción: Registra eventos del pipeline con handlers para archivo y consola.
"""
import logging
import time
import os
from typing import Callable, Any
from functools import wraps
from logging.handlers import RotatingFileHandler


def setup_logger(name: str = "Orders_Pipeline", log_file: str = "logs/pipeline.log",
    level: int = logging.INFO,max_file_size: int = 10 * 1024 * 1024,  # 10 MB size
    backup_count: int = 3
) -> logging.Logger:
    """
    Configura un logger con handlers para archivo (con rotación) y consola.
    
    Args:
        name: Nombre del logger
        log_file: Ruta del archivo de log
        level: Nivel de logging (INFO, DEBUG, etc.)
        max_file_size: Tamaño máximo del archivo de log antes de rotar
        backup_count: Número de archivos de backup a mantener
        
    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Si ya está configurado, retornar el existente
    if logger.handlers:
        return logger
    
    # Establecer nivel
    logger.setLevel(level)
    
    # Crear directorio de logs si no existe
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Formato común
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 1. Handler para rotación de archivo.
    file_handler = RotatingFileHandler(filename=log_file,maxBytes=max_file_size,backupCount=backup_count,
        encoding='utf-8')

    file_handler.setLevel(logging.DEBUG)  # Nivel más detallado para archivo
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 2. Handler para CONSOLA
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Solo INFO+ para consola
    console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
    logger.addHandler(console_handler)
    
    logger.debug(f"Logger '{name}' configurado. Archivo: {log_file}")
    
    return logger

def log_execution(func: Callable) -> Callable:
    """
    Decorador que registra el tiempo de ejecución de una función.

    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger = logging.getLogger("Orders_Pipeline")
        logger.info(f"Iniciando: {func.__name__}")
        
        start_time = time.perf_counter()  # Más preciso que time.time()
        
        try:
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start_time
            
            logger.info(f"Completado: {func.__name__} en {elapsed:.4f} segundos")
            return result
            
        except Exception as e:
            elapsed = time.perf_counter() - start_time
            logger.error(
                f"Falló: {func.__name__} después de {elapsed:.4f} segundos. "
                f"Error: {str(e)}", 
                exc_info=True
            )
            raise
    
    return wrapper

# Logger global para el pipeline
logger = setup_logger()