# PARTE 1 – Diseño y Razonamiento del Golden Record
## Selección de Campos:
### Campos descartados y fundamentación
* __Eliminación obligatoria de email y telefono.__
En Ecuador, estos datos están protegidos por:
    Artículo 66 de la Constitución: Derecho a la protección de datos personales.
    Ley Orgánica de Protección de Datos Personales (LOPDP): Exige tratamiento adecuado de información personal.
    Principio de Minimización: Solo recolectar datos estrictamente necesarios.

* __Campos técnicos obsoleto__
Se entiende que los campos internal_legacy_flag corresponde Sistemas Legacy, tecnología que no es utilizada al día de hoy.

* __Referencias internas de sistema__
Valores operativos, que si bien tienen un objetivo en los procesos internos de las empresas, carecen de validez analítica.

* __Datos temporales__
Si bien el control de inventario y rotación de productos son un motivo para promover la compra de productos, el nivel de stock en un momento específico y su volatilidad no resultan en una variable a considerar en modelos predictivos.

## Campos con transformación
* Price (de products.json)
Conversión de string a float con manejo de símbolos de moneda ($, €, £) y eliminación de separadores de miles. Validación de valores negativos o cero. Redondeo a 2 decimales para consistencia monetaria.

* Qty (de orders.json) y signup_date (de users.json)
Validación de valores nulos,y asignación de cantidades de ser necesario como el caso de cantidad ordenadas.

* User_id y Product_id (de orders.json)
Validación de integridad, órdenes referenciado a usuarios o productos inexistentes.

* Order_id (de orders.json)
Detección y manejo de duplicados manteniendo el más reciente.

## Campos calculados
* Total_price
Monto total de la orden.

* Observations
Metadata que documenta problemas de calidad sin eliminar registros.

* Valid_orden
Entrada que no presenta ninguna observación ni anomalía.

## Esquema final:
    {
        "order_id": "string", 
        "user_id": "string",
        "user_name": "string",
        "product_id": "string",
        "product_name": "string",
        "product_category": "string",
        "qty": "integer",
        "unit_price": "float",
        "total_price": "float",
        "transaction_date": "datetime",
        "valid_order": "boolean",
        "observations": []
    }

## Integridad de Datos - Estrategia
### Estrategia General
No descartar el ingreso de datos, transformarlos a su forma útil de manera analítica notificando al usuario a través del log.

### Matriz de Decisiones

| Problema             | Acción                        | Alerta           | Ejemplo                                |
|----------------------|-------------------------------|------------------|----------------------------------------|
| Valores nulos        | Valor por defecto | WARNING          | `qty: null → 1`                        |
| Formatos incorrectos    | Conversión automática         | INFO             | `price: "25.50" → 25.50`               |
| Referencias inválidas| Crear placeholder + flag      | WARNING + flag   | `user_id "u99" → flag "SIN_USUARIO"`   |
| Valores fuera de rango | Mantener + flag             | WARNING + flag   | `price ≤ 0 → flag "PRECIO_INVALIDO"`   |
| Duplicados           | Conservar último              | WARNING          | `order_id "o503" duplicado`            |

Desde la perspectiva de Data Science, este enfoque genera un dataset enriquecido con metadata que da lugar a filtrar y ponderar según los objetivos del modelo.

# PARTE 2 – Requisitos técnicos
## 1. Logging
Implementado en src/pipeline/log_setup.py. Se hace uso de un Logger con handlers para archivo y consola.

## 2. Manejo de errores
Implementado en todos los módulos, implementación de FileNotFoundError, JSONDecodeError, ValueError.

## 3. Modularidad
### Asignación de responsabilidades en la estructura del proyecto:
```python
orders_enrichment_pipeline
├── data
│   ├── output
│   │   └── enriched_orders.json
│   └── raw
│       ├── orders.json
│       ├── products.json
│       └── users.json
├── docs
│   ├── ANSWERS.md
│   └── README.md
├── logs
│   └── pipeline.log
├── requirements.txt
└── src
    ├── main.py
    └── pipeline
        ├── data_structure.py (dataclasses)
        ├── enrich.py
        ├── in_out.py
        ├── log_setup.py
        └── transform.py
```
        
### Principios aplicados:
* Single Responsibility: Cada módulo tiene una única responsabilidad.
* Open/Closed: Extensiones posibles sin modificar código existente.
* Dependency Inversion: Interfaces claras entre módulos.
* Clean Code: Convención snakecase y Docstrings explicativos

# PARTE 3 -Escenario de escalabilidad
En el escenario en mención, el escalado de hardware en un único equipo presenta serias limitaciones físicas y económicas. En este caso en específico, la solución más probablemente efectiva es implementar una arquitectura de contenedores. Esta división de la lógica de procesamiento permite que cada componente cuente con sus propios recursos aislados y por ende una performance optimizada.