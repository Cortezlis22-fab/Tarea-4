Proyecto: Normalización y Exploración de Transacciones Multifuente
Herramienta de desarrollo: Python y Visual Studio Code
1. Diseño y decisiones del estudiante
El sistema se organizó en módulos independientes para facilitar su comprensión y mantenimiento: normalizer.py transforma los registros, validator.py verifica su integridad, metrics.py calcula resultados, interface.py permite explorarlos y main.py coordina la ejecución.

El estudiante definió y adoptó el modelo normalizado común con los campos id, amount, currency, timestamp, status y source. También estableció las reglas de transformación y validación que utiliza el proyecto y las registró en config/rules.json para que puedan revisarse o modificarse sin cambiar la lógica principal.

Las decisiones aplicadas son: aceptar USD y EUR; convertir montos de centavos a unidades monetarias; interpretar el formato decimal europeo de la tercera fuente; expresar las fechas en ISO-8601; y unificar los estados en SUCCESS, FAILED o PENDING. Se consideran inválidos los registros con campos obligatorios ausentes o vacíos, monto no numérico, no finito o menor o igual a cero, moneda no admitida, estado no reconocido o fecha inválida. Los registros inválidos se separan y se muestran con sus errores; no se eliminan silenciosamente. Los importes se mantienen agrupados por moneda y no se suman divisas diferentes.
2. Uso de inteligencia artificial
La IA se utilizó como apoyo para estructurar el código, proponer alternativas de lectura y procesamiento de JSON, sugerir lógica de parsing y validación, asistir en la organización de los módulos y apoyar la creación de la interfaz de consola. También se utilizó para explicar errores encontrados durante la implementación.

La IA no tuvo autoridad para establecer las decisiones finales del proyecto. El estudiante revisó las sugerencias y asumió la responsabilidad de definir y aprobar el esquema de datos, las reglas de normalización y los criterios para considerar una transacción válida o inválida. Las reglas finales se encuentran explícitas en config/rules.json y los criterios de validación están implementados en src/validator.py.
3. Verificación
Se probaron registros de las tres fuentes y casos con moneda no soportada, estado desconocido, fecha incorrecta, monto negativo e identificador vacío. Además, se prepararon pruebas automatizadas con unittest para comprobar la normalización y la validación. La interfaz CLI permite listar transacciones válidas, filtrar por estado o moneda, consultar métricas y revisar los registros inválidos.

Conclusión: El sistema convierte registros heterogéneos a una estructura común, valida los datos, genera métricas por moneda y permite su exploración. Las decisiones técnicas finales son responsabilidad del estudiante y quedan reflejadas en la configuración y el código fuente.