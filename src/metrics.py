
from collections import defaultdict
from decimal import Decimal


def calculate_metrics(total_processed, valid_transactions, invalid_count):
    """
    Calcula las métricas generales de las transacciones.
    Los totales monetarios se calculan únicamente
    con transacciones válidas.
    """

    by_status = defaultdict(int)

    by_currency = defaultdict(
        lambda: {
            "count": 0,
            "total": Decimal("0.00")
        }
    )

    # Recorrer las transacciones válidas
    for transaction in valid_transactions:

        status = transaction["status"]
        currency = transaction["currency"]
        amount = Decimal(str(transaction["amount"]))

        # Contabilizar estados
        by_status[status] += 1

        # Contabilizar monedas y sumar sus montos
        by_currency[currency]["count"] += 1
        by_currency[currency]["total"] += amount

    # Preparar el resultado de las métricas
    metrics = {
        "total_processed": total_processed,
        "valid": len(valid_transactions),
        "invalid": invalid_count,
        "by_status": dict(by_status),
        "by_currency": {}
    }

    for currency, data in by_currency.items():

        metrics["by_currency"][currency] = {
            "count": data["count"],
            "total": f"{data['total']:.2f}"
        }

    return metrics
