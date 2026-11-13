
from datetime import datetime
from math import isfinite


def validate_transaction(transaction, rules):
    """
    Valida una transacción normalizada.
    Devuelve una lista con los errores encontrados.
    """

    errors = []

    if not isinstance(transaction, dict):
        return ["La transacción no tiene un formato válido"]

    # 1. Verificar campos obligatorios
    required_fields = [
        "id",
        "amount",
        "currency",
        "timestamp",
        "status",
        "source"
    ]

    for field in required_fields:
        if field not in transaction:
            errors.append(f"Falta el campo obligatorio: {field}")

        elif transaction[field] is None or transaction[field] == "":
            errors.append(f"El campo {field} está vacío")

    # 2. Validar identificador
    identifier = transaction.get("id")

    if not isinstance(identifier, str) or not identifier.strip():
        errors.append("El identificador no es válido")

    # 3. Validar monto
    amount = transaction.get("amount")

    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        errors.append("El monto debe ser numérico")

    elif not isfinite(amount):
        errors.append("El monto debe ser un número finito")

    elif amount <= 0:
        errors.append("El monto debe ser mayor que cero")

    # 4. Validar moneda
    currency = transaction.get("currency")

    supported_currencies = rules["currencies"]["supported"]

    if currency not in supported_currencies:
        errors.append(f"Moneda no soportada: {currency}")

    # 5. Validar estado
    status = transaction.get("status")

    allowed_statuses = rules["statuses"]["allowed"]

    if status not in allowed_statuses:
        errors.append(f"Estado no permitido: {status}")

    # 6. Validar fecha
    timestamp = transaction.get("timestamp")

    if isinstance(timestamp, str):
        try:
            datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )
        except ValueError:
            errors.append("La fecha no tiene un formato ISO-8601 válido")
    else:
        errors.append("La fecha debe ser texto")

    # 7. Validar fuente
    source = transaction.get("source")

    if source not in rules["sources"]:
        errors.append(f"Fuente desconocida: {source}")

    return errors


def validate_transactions(transactions, rules):
    """
    Separa las transacciones válidas de las inválidas.
    """

    valid = []
    invalid = []

    for transaction in transactions:

        errors = validate_transaction(transaction, rules)

        if errors:
            invalid.append({
                "transaction": transaction,
                "errors": errors
            })

        else:
            valid.append(transaction)

    return {
        "valid": valid,
        "invalid": invalid
    }
