
import json
from pathlib import Path

from interface import run_interface
from normalizer import normalize_transaction
from validator import validate_transactions
from metrics import calculate_metrics


# Obtener la ruta principal del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent


def load_json(file_path):
    """Lee un archivo JSON."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    """Ejecuta el sistema de normalización, validación y métricas."""

    print("=" * 55)
    print(" SISTEMA DE NORMALIZACIÓN DE TRANSACCIONES")
    print("=" * 55)

    transactions_path = BASE_DIR / "data" / "transactions.json"
    rules_path = BASE_DIR / "config" / "rules.json"

    try:
        # 1. Leer los archivos
        transactions = load_json(transactions_path)
        rules = load_json(rules_path)

        print("\nArchivos cargados correctamente.")

        # 2. Normalizar las transacciones
        normalized = []
        invalid = []

        for transaction in transactions:
            try:
                result = normalize_transaction(transaction, rules)
                normalized.append(result)

            except (ValueError, KeyError, TypeError, ArithmeticError) as error:
                invalid.append({
                    "transaction": transaction,
                    "errors": [str(error)]
                })

        # 3. Validar las transacciones normalizadas
        validation = validate_transactions(normalized, rules)

        valid = validation["valid"]
        invalid.extend(validation["invalid"])

        # 4. Mostrar las transacciones válidas
        print("\nTRANSACCIONES VÁLIDAS")
        print("-" * 55)

        for transaction in valid:
            print(json.dumps(
                transaction,
                indent=4,
                ensure_ascii=False
            ))
            print("-" * 55)

        # 5. Mostrar las transacciones inválidas
        print("\nTRANSACCIONES INVÁLIDAS")
        print("-" * 55)

        if not invalid:
            print("No se encontraron transacciones inválidas.")

        for item in invalid:
            print("Transacción:")
            print(json.dumps(
                item["transaction"],
                indent=4,
                ensure_ascii=False
            ))

            print("Errores encontrados:")

            for error in item["errors"]:
                print(f" - {error}")

            print("-" * 55)

        # 6. Calcular métricas
        metrics = calculate_metrics(
            len(transactions),
            valid,
            len(invalid)
        )
        # Iniciar la interfaz interactiva
        run_interface(valid, invalid, metrics)

        # 7. Mostrar resumen
        print("\nRESUMEN DEL PROCESAMIENTO")
        print("=" * 55)

        print(f"Total procesadas: {metrics['total_processed']}")
        print(f"Total válidas: {metrics['valid']}")
        print(f"Total inválidas: {metrics['invalid']}")

        # 8. Mostrar conteo por estado
        print("\nTRANSACCIONES POR ESTADO")
        print("-" * 55)

        for status, count in metrics["by_status"].items():
            print(f"{status}: {count}")

        # 9. Mostrar totales por moneda
        print("\nTOTALES POR MONEDA")
        print("-" * 55)

        for currency, data in metrics["by_currency"].items():
            print(f"Moneda: {currency}")
            print(f"Cantidad de transacciones: {data['count']}")
            print(f"Total: {data['total']}")
            print("-" * 55)

    except FileNotFoundError as error:
        print(f"\nError: No se encontró el archivo: {error}")

    except json.JSONDecodeError as error:
        print(f"\nError al leer el JSON: {error}")

    except (TypeError, KeyError) as error:
        print(f"\nError en la configuración: {error}")


if __name__ == "__main__":
    main()
