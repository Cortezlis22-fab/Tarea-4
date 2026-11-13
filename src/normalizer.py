
from datetime import datetime
from decimal import Decimal, InvalidOperation


def detect_source(transaction, rules):
    """
    Identifica la fuente de una transacción
    mediante su campo identificador.
    """
    for source_name, source_rules in rules["sources"].items():
        identifier = source_rules["identifier"]

        if identifier in transaction:
            return source_name, source_rules

    raise ValueError("No se pudo identificar la fuente")


def normalize_amount(value, amount_format):
    """
    Convierte los montos a un formato decimal común.
    """
    amount = str(value).strip()

    if amount_format == "cents":
        return Decimal(amount) / Decimal("100")

    elif amount_format == "european":
        amount = amount.replace("€", "").replace(" ", "")
        amount = amount.replace(".", "").replace(",", ".")
        return Decimal(amount)

    elif amount_format == "decimal":
        return Decimal(amount)

    raise ValueError("Formato de monto desconocido")


def normalize_currency(transaction, source_rules, rules):
    """
    Identifica y normaliza el código de moneda.
    """
    currency_field = source_rules["currency_field"]

    if currency_field and transaction.get(currency_field):
        original_currency = str(
            transaction[currency_field]
        ).strip()
    else:
        amount = str(
            transaction[source_rules["amount_field"]]
        )

        if "€" in amount:
            original_currency = "€"
        elif "$" in amount:
            original_currency = "$"
        else:
            raise ValueError("No se pudo identificar la moneda")

    aliases = rules["currencies"]["aliases"]

    currency = aliases.get(original_currency)

    if currency is None:
        currency = aliases.get(original_currency.lower())

    if currency not in rules["currencies"]["supported"]:
        raise ValueError(f"Moneda no soportada: {original_currency}")

    return currency


def normalize_date(value, rules):
    """
    Convierte diferentes formatos de fecha
    al formato ISO-8601 establecido.
    """
    for date_format in rules["dates"]["formats"]:
        try:
            parsed_date = datetime.strptime(
                str(value), date_format
            )

            return parsed_date.strftime(
                rules["dates"]["output_format"]
            )

        except ValueError:
            continue

    raise ValueError(f"Formato de fecha no válido: {value}")


def normalize_status(value, rules):
    """
    Unifica los estados de las transacciones.
    """
    mapping = rules["statuses"]["mapping"]

    status = mapping.get(str(value).strip().lower())

    if status is None:
        raise ValueError(f"Estado desconocido: {value}")

    return status


def normalize_transaction(transaction, rules):
    """
    Transforma una transacción individual
    al modelo de datos normalizado.
    """
    source_name, source_rules = detect_source(
        transaction, rules
    )

    identifier = str(
        transaction[source_rules["identifier"]]
    )

    amount = normalize_amount(
        transaction[source_rules["amount_field"]],
        source_rules["amount_format"]
    )

    currency = normalize_currency(
        transaction, source_rules, rules
    )

    timestamp = normalize_date(
        transaction[source_rules["date_field"]],
        rules
    )

    status = normalize_status(
        transaction[source_rules["status_field"]],
        rules
    )

    return {
        "id": identifier,
        "amount": float(amount),
        "currency": currency,
        "timestamp": timestamp,
        "status": status,
        "source": source_name
    }


def normalize_transactions(transactions, rules):
    """
    Normaliza una lista completa de transacciones.
    """
    normalized = []

    for transaction in transactions:
        normalized.append(
            normalize_transaction(transaction, rules)
        )

    return normalized
