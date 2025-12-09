"""
Módulo de Entrada/Salida de Datos
----------------
Fecha: 2025-12-08
Descripción: Lee y escribe archivos json.
"""
import json
from dataclasses import asdict
from typing import List
from src.pipeline.log_setup import logger, log_execution

@log_execution
def load_json(filepath: str) -> List[dict]:
    """Carga y valida un archivo json desde una ruta específica."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                # Manejo de error si el json no es una lista de objetos
                raise ValueError(f"El formato de {filepath} debe ser una lista de objetos json.")
            return data
    except json.JSONDecodeError as e:
        # Manejo de error si el formato interno de json es incorrecto
        logger.error(f"Error decodificando json en {filepath}: {e}")
        raise

@log_execution
def save_json(data: List[object], filepath: str):
    """Guarda una lista de objetos (dataclasses) en un archivo json."""
    try:
        # Convertimos las dataclasses a diccionarios para json
        output_data = [asdict(record) for record in data]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=4)
        logger.info(f"Archivo guardado exitosamente: {filepath}")
    except Exception as e:
        logger.error(f"Error guardando archivo {filepath}: {e}")
        raise