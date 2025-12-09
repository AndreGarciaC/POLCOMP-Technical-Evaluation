"""
Módulo de Transformación.
----------------
Fecha: 2025-12-09
Descripción: Limpieza de datos y obtiene cálculos derivados.
"""
from typing import Any
from src.pipeline.log_setup import logger

def clean_price(price_input: Any) -> float:
    """Convierte precios a flotante."""
    if price_input is None:
        return 0.0

    if isinstance(price_input, str):
        # Remover símbolos de moneda y separadores de miles
        price_input = price_input.strip()
        for char in ['$', '€', '£', ',', ' ']:
            price_input = price_input.replace(char, '')
    
    try:
        val = float(price_input)
        
        # Validaciones
        if val < 0:
            logger.warning(f"Precio negativo: {val}. Convirtiendo a 0.0")
            return 0.0
        elif val == 0:
            logger.debug(f"Precio cero detectado")
            return 0.0
        elif val > 1000000:  # Límite razonable
            logger.warning(f"Precio sospechosamente alto: {val}")
        
        return round(val, 2)  # Redondear a 2 decimales
        
    except (ValueError, TypeError) as e:
        logger.warning(f"Precio inválido '{price_input}': {e}. Usando 0.0")
        return 0.0

def clean_qty(qty_input: Any) -> int:
    """Convierte cantidad a un entero seguro para órdenes."""
    if qty_input is None:
        logger.debug("Cantidad nula")
        return 1 
    
    try:
        if isinstance(qty_input, str):
            qty_input = qty_input.strip()
            try:
                qty_input = float(qty_input)
            except ValueError:
                pass
        
        val = int(float(qty_input)) if isinstance(qty_input, (int, float, str)) else int(qty_input)
        
        if val <= 0:
            logger.warning(f"Cantidad inválida: {val}. Se usa 1")
            return 1
        
        return val
        
    except (ValueError, TypeError) as e:
        logger.warning(f"Cantidad inválida '{qty_input}': {e}. Se usa 1")
        return 1