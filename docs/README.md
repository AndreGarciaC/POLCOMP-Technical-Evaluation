# Prueba Técnica: DESARROLLADOR DEL DEPARTAMENTO DE INNOVACIÓN Y TECNOLOGÍA

## 1. Contexto del Negocio
Trabajas como Desarrollador en una empresa de E-Commerce.

El equipo de innovación y tecnología está construyendo un nuevo modelo de recomendación y necesita un dataset consolidado ("Golden Record") de las transacciones recientes.

Actualmente, la información reside en tres sistemas legados diferentes que exportan datos en formato JSON de manera periódica. La misión del candidato será construir un proceso robusto que unifique estos datos, aplique reglas de negocio y genere un archivo limpio y enriquecido para el consumo analítico.


## 2. Fuentes de Datos (Input)
Para realizar el ejercicio, puedes crear tres archivos locales (users.json, products.json, orders.json) con la siguiente data de muestra:
A. users.json (Clientes)
Nota: Contiene información sensible y campos técnicos obsoletos.

[

  {"id": "u1", "name": "Alice", "email": "alice@example.com", "signup_date": "2023-01-15", "internal_legacy_flag": "X99", "phone": "555-0101"},

  {"id": "u2", "name": "Bob", "email": "bob@example.com", "signup_date": "2023-02-20", "internal_legacy_flag": "X99", "phone": "555-0202"},

  {"id": "u3", "name": "Charlie", "email": "charlie@example.com", "signup_date": "2023-03-10", "internal_legacy_flag": "Y00", "phone": null},

  {"id": "u4", "name": "Diana", "email": "diana@example.com", "signup_date": null, "internal_legacy_flag": "Y00", "phone": "555-0404"},

  {"id": "u5", "name": "Eve", "email": "eve@example.com", "signup_date": "2024-05-01", "internal_legacy_flag": null, "phone": "555-0505"}

]
B. products.json (Catálogo)
[

  {"id": "p100", "name": "Laptop Pro", "category": "Electronics", "price": 1200.00, "stock": 50, "supplier_id_internal": 778},

  {"id": "p101", "name": "Wireless Mouse", "category": "Electronics", "price": "25.50", "stock": 200, "supplier_id_internal": 779},

  {"id": "p102", "name": "Coffee Mug", "category": "Home", "price": 15.00, "stock": 100, "supplier_id_internal": 780},

  {"id": "p103", "name": "Book: Data Eng.", "category": "Books", "price": null, "stock": 500, "supplier_id_internal": 781},

  {"id": "p104", "name": "T-Shirt Promo", "category": "Apparel", "price": 0.00, "stock": 0, "supplier_id_internal": 782}

]
C. orders.json (Transacciones)
[

  {"order_id": "o500", "user_id": "u1", "product_id": "p100", "qty": 1, "timestamp": "2023-10-27T10:00:00"},

  {"order_id": "o501", "user_id": "u2", "product_id": "p101", "qty": 2, "timestamp": "2023-10-27T11:30:00"},

  {"order_id": "o502", "user_id": "u99", "product_id": "p100", "qty": 1, "timestamp": "2023-10-27T12:00:00"}, 

  {"order_id": "o503", "user_id": "u3", "product_id": "p102", "qty": null, "timestamp": "2023-10-27T13:00:00"}, 

  {"order_id": "o504", "user_id": "u4", "product_id": "p999", "qty": 1, "timestamp": "2023-10-27T14:00:00"}, 

  {"order_id": "o503", "user_id": "u3", "product_id": "p102", "qty": 3, "timestamp": "2023-10-27T13:00:01"}, 

  {"order_id": "o505", "user_id": "u5", "product_id": "p104", "qty": 5, "timestamp": "2023-10-27T15:00:00"}

]


Desafío Técnico a Desarrollar
El ejercicio consta de tres partes obligatorias.
#PARTE 1 – Diseño y Razonamiento (Documentación)
El candidato deberá documentar: Selección de Campos -Definir el esquema final del JSON de salida. -Indicar qué campos se eliminan y justificar por qué. -Indicar qué campos se descartan, se procesan parcialmente o se alertan. -Indicar si se añaden campos calculados.

Integridad de Datos -Explicar la estrategia para manejar datos erróneos. -Definir si se deben descartar, procesar parcialmente o generar alertas. -Justificar las decisiones desde la perspectiva del equipo de Data Science.
#Parte 2: Implementación del Pipeline (Código Python)
Escribe un script en Python que realice lo siguiente:
Ingesta
Lee los tres archivos JSON.
Enriquecimiento
Cruza la información para tener una vista completa de la orden (Datos del usuario + Datos del producto + Datos de la transacción).
Transformación
Asegura que los tipos de datos sean correctos.
Implementa las decisiones de campos que tomaste en la Parte 1.
Calcula el valor total de la orden (price * qty).
Output
Guarda el resultado en un archivo enriched_orders.json.


Requisitos Técnicos (Buenas Prácticas)
Logging: Implementa logs reales (librería logging), indicando inicio del proceso, progreso y errores/warnings. Evita usar print().
Manejo de Errores: El script no debe romperse si falta un archivo o si un formato es inválido; debe manejar la excepción y fallar/avisar elegantemente.
Modularidad: Organiza el código en funciones o clases claras, siguiendo principios como SOLID o Clean Code.
Librerías: Puedes usar Python estándar o librerías como Pandas/Polars. Si usas librerías externas, incluye un requirements.txt.


#Parte 3: Escenario de Escalabilidad (Teórico)
Supongamos que el negocio crece y el archivo orders.json ahora pesa 50 GB y llega cada hora. Tu script actual se queda sin memoria (OOM) al intentar cargarlo.

Sin escribir código, explica brevemente:

¿Cómo modificarías tu enfoque o arquitectura para procesar este volumen de datos sin aumentar infinitamente la RAM del servidor?


## 4. Criterios de Evaluación
No solo buscamos que el código "corra". Evaluaremos:

Calidad del Código: Legibilidad, nombres de variables, estructura y tipado.
Buenas Prácticas: Uso correcto de logs, manejo de excepciones y estructura del proyecto.
Razonamiento de Negocio: La lógica detrás de qué campos guardar (ej: manejo de PII) y cómo tratar datos faltantes.
Conocimiento de Arquitectura: La respuesta sobre escalabilidad.


Entregables
Código fuente (.py).
Archivo de salida generado (enriched_orders.json).
Respuestas a las preguntas de razonamiento y escalabilidad (puede ser un ANSWERS.md o dentro del mismo script como comentarios de bloque).

