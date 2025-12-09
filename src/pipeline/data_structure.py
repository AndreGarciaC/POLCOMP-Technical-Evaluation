"""
Módulo de Estructuración y Validación de Datos
----------------
Fecha: 2025-12-08
Descripción: Organiza la raw data y la estructura bajo un mismo modelo para su procesamiento.
"""

from dataclasses import dataclass, field
from typing import Optional

# Una dataclass es para cuando el propósito principal de una clase es ser un contenedor de valores.
# INPUTS
@dataclass
class User:
    id: str
    name: str
    signup_date: Optional[str]

@dataclass
class Product:
    id: str
    name: str
    product_category: str
    price: float
    stock: int

@dataclass
class Order:
    order_id: str
    user_id: str
    product_id: str
    qty: int
    timestamp: str

# OUTPUT - GOLDEN RECORD
@dataclass
class EnrichedOrder:
    """Estructura final con datos combinados"""
    order_id: str
    user_id: str
    user_name: str
    product_id: str
    product_name: str
    product_category: str
    qty: int
    unit_price: float
    total_price: float
    transaction_date: str
    order_valid: bool
    # Campo extra
    observations: list[str] = field(default_factory=list)