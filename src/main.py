"""
Módulo Main
----------------
Fecha: 2025-12-09
Descripción: Ejecuta el pipeline.
"""
import sys
import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_OUTPUT_DIR = BASE_DIR / "data" / "output"

sys.path.append(str(BASE_DIR))


from src.pipeline.in_out import load_json, save_json
from src.pipeline.enrich import build_lookup_tables, process_orders
from src.pipeline.log_setup import logger

def validate_input_files() -> bool:
    """
    Valida que todos los archivos json requeridos existan.
    
    Returns:
        bool: True si todos los archivos existen, False en caso contrario.
    """
    required_files = ["users.json", "products.json", "orders.json"]
    
    for file_name in required_files:
        file_path = DATA_RAW_DIR / file_name
        if not file_path.exists():
            logger.error(f"Archivo json faltante: {file_path}")
            logger.error(f"Cargue los archivos correctos en {DATA_RAW_DIR}")
            return False
    
    return True

def main():
    """
    Función principal que ejecuta el pipeline completo.    
    """
    try:
        logger.info("INICIA PIPELINE")

        logger.info("Validando archivos de entrada...")
        if not validate_input_files():
            logger.critical("Fallo en validación de archivos.")
            sys.exit(1)
        
        # 1. INGRESO DE INNFORMACIÓN
        users_raw = load_json(os.path.join(DATA_RAW_DIR, "users.json"))
        products_raw = load_json(os.path.join(DATA_RAW_DIR, "products.json"))
        orders_raw = load_json(os.path.join(DATA_RAW_DIR, "orders.json"))
        
        # 2. CREA ESTRUCTURAS DE DATOS ENRIQUECIDOS
        users_map, products_map = build_lookup_tables(users_raw, products_raw)
        enriched_orders = process_orders(orders_raw, users_map, products_map)
        
        # 3. ALMACENA RESULTADOS
        output_path = DATA_OUTPUT_DIR / "enriched_orders.json"
        DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True) 
        save_json(enriched_orders, output_path)
        
        logger.info("FINALIZA PIPELINE EXITOSAMENTE")

    except FileNotFoundError as e:
        logger.critical(f"Error de archivo no encontrado: {e}")
        sys.exit(1)    
    except Exception as e:
        # Si load_json o save_json fallan, el error se registra en log.py y el programa termina
        logger.critical(f"El pipeline falló de forma crítica y se detuvo: {e}")
        sys.exit(1) # Terminamos el proceso con código de error

if __name__ == "__main__":
    main()