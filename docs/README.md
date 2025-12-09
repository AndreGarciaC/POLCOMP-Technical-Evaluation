# Data Orders Enrichment Pipeline

## Objetivo Técnico
Este repositorio contiene una solución técnica evaluable para consolidación de órdenes de e-commerce, enriquecimiento, validación y exportación a un JSON limpio.

Se utiliza la librería estándar logging de Python para trazabilidad, reemplazando print

Data Flow
Ingestion: Read JSON files from data/raw/

Transformation: Clean, validate, type conversion

Enrichment: Join user/product data, calculate totals

Output: Write to data/output/enriched_orders.json

LOGGING
es un modulo robousto de python útil porque permite controlar el nivel de importancia del mensaje (INFO, WARNING, ERROR)


Manejo robusto de paths con pathlib

en Ecuador el email es legalmente considerado un dato personal y está protegido por la Constitución y la Ley Orgánica de Protección de Datos Personales

el uso de diccionarios Esto hace que buscar por ID sea INSTANTÁNEO y no lento (crucial para escalabilidad)

en enriched
# 1. Manejo de Órdenes Duplicadas (o503 aparece dos veces)
    # Estrategia: Nos quedamos con la última versión de la orden (o la que tiene datos más completos/recientes)