
# Sistema de Normalización y Exploración de Transacciones Multifuente

## 1. Descripción

Aplicación desarrollada en Python para procesar transacciones provenientes de diferentes fuentes y estructuras de datos. El sistema transforma los registros a un modelo común, valida su información, calcula métricas y permite explorar los resultados mediante una interfaz interactiva de consola.

## 2. Objetivos

- Identificar transacciones de diferentes fuentes.
- Normalizar montos, monedas, fechas y estados.
- Detectar transacciones inválidas o incompletas.
- Generar métricas por estado y moneda.
- Permitir listar y filtrar transacciones.

## 3. Tecnologías utilizadas

- Python 3.
- JSON.
- Unittest.
- Visual Studio Code.

## 4. Estructura del proyecto

```text
Normalizacion_Transacciones/
├── config/
│   └── rules.json
├── data/
│   ├── transactions.json
│   └── transactions_test.json
├── src/
│   ├── interface.py
│   ├── main.py
│   ├── metrics.py
│   ├── normalizer.py
│   └── validator.py
├── tests/
│   └── test_normalizer.py
├── README.md
├── NOTA_TECNICA.md
└── requirements.txt
```

## 5. Descripción de los módulos

| Módulo | Responsabilidad |
|---|---|
| normalizer.py | Identifica fuentes y transforma transacciones. |
| validator.py | Valida los registros y detecta errores. |
| metrics.py | Calcula métricas y totales por moneda. |
| interface.py | Permite explorar y filtrar los datos. |
| main.py | Coordina la ejecución del sistema. |

El archivo `rules.json` contiene las reglas de configuración de monedas, estados, fechas y estructuras de las fuentes.

## 6. Modelo normalizado

Las transacciones se convierten a una estructura común:

- id: identificador de la transacción.
- amount: monto numérico.
- currency: código de moneda.
- timestamp: fecha en formato ISO-8601.
- status: estado normalizado.
- source: fuente de origen.

Los estados permitidos son SUCCESS, FAILED y PENDING. Las monedas configuradas son USD y EUR.

## 7. Ejecución del proyecto

Requisito: tener Python 3 instalado.

Desde la terminal, ubicarse en la carpeta principal y ejecutar:

```bash
python src/main.py
```

## 8. Opciones de la interfaz

1. Listar transacciones válidas.
2. Filtrar por estado.
3. Filtrar por moneda.
4. Consultar métricas.
5. Consultar transacciones inválidas.
0. Salir.

## 9. Pruebas automatizadas

Ejecutar las pruebas mediante:

```bash
python -m unittest discover -s tests -v
```

Las pruebas verifican la normalización de las fuentes, conversión de datos, validación y detección de errores.

## 10. Consideraciones

Los montos se calculan por separado según su moneda. El sistema no realiza conversiones cambiarias entre divisas.

Las transacciones inválidas se conservan con sus respectivos mensajes de error para facilitar su revisión.

