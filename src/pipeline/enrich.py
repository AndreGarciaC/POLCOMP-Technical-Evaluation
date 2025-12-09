"""
Módulo de Enriquecimiento de Órdenes
----------------
Fecha: 2025-12-09
Descripción: Aplica reglas de negocio para la combinación de datos.
"""
from typing import List, Dict
from src.pipeline.data_structure import User, Product, EnrichedOrder
from src.pipeline.transform import clean_price, clean_qty
from src.pipeline.log_setup import logger, log_execution

@log_execution
def build_lookup_tables(users_raw: List[dict], products_raw: List[dict]):
    """
    Crea diccionarios de Usuarios y Productos. Id de usuario como key.
    """
    users_map = {}
    for u in users_raw:
        # Se remueve información sensible o nula.
        users_map[u['id']] = User(
            id=u['id'], 
            name=u['name'],
            signup_date=u.get('signup_date')
        )
        if u.get('signup_date') is None:
            logger.debug(f"Usuario {u['id']} no tiene fecha de registro")

    products_map = {}
    for p in products_raw:
        cleaned_price = clean_price(p['price'])
        if cleaned_price <= 0:
            logger.warning(f"Producto {p['id']} tiene precio {cleaned_price}")
        products_map[p['id']] = Product(
            id=p['id'],
            name=p['name'],
            product_category=p['category'],
            price=cleaned_price,
            stock=int(p['stock'] if p['stock'] else 0)
        )
        
    return users_map, products_map

@log_execution
def process_orders(orders_raw: List[dict], users_map: Dict[str, User], products_map: Dict[str, Product]) -> List[EnrichedOrder]:
    enriched_data = []
    
    # 1. Manejo de órdenes duplicadas
    unique_orders = {o['order_id']: o for o in orders_raw if o.get('order_id')}

    # 2. Enriquecimiento de órdenes
    for order_data in unique_orders.values():
        flags = []
        user_id = order_data.get('user_id')
        product_id = order_data.get('product_id')
        qty = clean_qty(order_data.get('qty'))
        
        user = users_map.get(user_id)
        product = products_map.get(product_id)

        # Si no existe usuario, agregamos la observación y se crea un registro genérico.
        if not user:
            logger.warning(f"Orden {order_data['order_id']} referencia usuario inexistente: {user_id}")
            flags.append("SIN_USUARIO")
            user = User(
                id=user_id or "DESCONOCIDO", 
                name="Usuario desconocido", 
                signup_date=None
            )
        
        # sI no existe producto, agregamos la observación y se crea un registro genérico.
        if not product:
            logger.warning(f"Orden {order_data['order_id']} referencia producto inexistente: {product_id}")
            flags.append("SIN_PRODUCTO")
            # Mantener el ID original
            product = Product(
                id=product_id or "DESCONOCIDO",  # ← Mantener ID original
                name="Producto desconocido", 
                product_category="Desconocido", 
                price=0.0, 
                stock=0
            )

        # Total
        total_price = round(product.price * qty, 2)

        # Golden record
        record = EnrichedOrder(
            order_id=order_data['order_id'],
            user_id=user.id,
            user_name=user.name, 
            product_id=product.id,
            product_name=product.name,
            product_category=product.product_category,
            qty=qty,
            unit_price=product.price,
            total_price=total_price,
            transaction_date=order_data.get('timestamp'),
            observations=flags
        )
        
        enriched_data.append(record)

    return enriched_data