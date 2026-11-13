
def show_transactions(transactions):
    """Muestra una lista de transacciones."""

    if not transactions:
        print("\nNo se encontraron transacciones.")
        return

    print("\nLISTADO DE TRANSACCIONES")
    print("-" * 55)

    for transaction in transactions:
        print(f"ID: {transaction['id']}")
        print(f"Monto: {transaction['amount']:.2f} {transaction['currency']}")
        print(f"Fecha: {transaction['timestamp']}")
        print(f"Estado: {transaction['status']}")
        print(f"Fuente: {transaction['source']}")
        print("-" * 55)


def filter_by_status(transactions):
    """Filtra transacciones por estado."""

    print("\nESTADOS DISPONIBLES")
    print("SUCCESS | FAILED | PENDING")

    status = input("Ingrese el estado que desea buscar: ").strip().upper()

    filtered = [
        transaction
        for transaction in transactions
        if transaction["status"] == status
    ]

    show_transactions(filtered)


def filter_by_currency(transactions):
    """Filtra transacciones por moneda."""

    print("\nMONEDAS DISPONIBLES")
    print("USD | EUR")

    currency = input("Ingrese la moneda que desea buscar: ").strip().upper()

    filtered = [
        transaction
        for transaction in transactions
        if transaction["currency"] == currency
    ]

    show_transactions(filtered)


def show_metrics(metrics):
    """Muestra las métricas del sistema."""

    print("\nRESUMEN DE MÉTRICAS")
    print("=" * 55)

    print(f"Total procesadas: {metrics['total_processed']}")
    print(f"Total válidas: {metrics['valid']}")
    print(f"Total inválidas: {metrics['invalid']}")

    print("\nTRANSACCIONES POR ESTADO")

    if not metrics["by_status"]:
        print("No hay datos disponibles.")
    else:
        for status, count in metrics["by_status"].items():
            print(f"{status}: {count}")

    print("\nTOTALES POR MONEDA")

    if not metrics["by_currency"]:
        print("No hay datos disponibles.")
    else:
        for currency, data in metrics["by_currency"].items():
            print(f"{currency}: {data['total']}")
            print(f"Cantidad: {data['count']}")


def show_invalid_transactions(invalid_transactions):
    """Muestra las transacciones que no superaron la validación."""

    print("\nTRANSACCIONES INVÁLIDAS")
    print("-" * 55)

    if not invalid_transactions:
        print("No se encontraron transacciones inválidas.")
        return

    for item in invalid_transactions:
        print("Registro:")
        print(item["transaction"])

        print("Errores:")
        for error in item["errors"]:
            print(f"- {error}")

        print("-" * 55)


def run_interface(valid_transactions, invalid_transactions, metrics):
    """Ejecuta el menú interactivo del sistema."""

    while True:

        print("\n" + "=" * 55)
        print(" SISTEMA DE EXPLORACIÓN DE TRANSACCIONES")
        print("=" * 55)

        print("1. Listar transacciones válidas")
        print("2. Filtrar por estado")
        print("3. Filtrar por moneda")
        print("4. Consultar métricas")
        print("5. Consultar transacciones inválidas")
        print("0. Salir")

        option = input("\nSeleccione una opción: ").strip()

        if option == "1":
            show_transactions(valid_transactions)

        elif option == "2":
            filter_by_status(valid_transactions)

        elif option == "3":
            filter_by_currency(valid_transactions)

        elif option == "4":
            show_metrics(metrics)

        elif option == "5":
            show_invalid_transactions(invalid_transactions)

        elif option == "0":
            print("\nGracias por utilizar el sistema.")
            break

        else:
            print("\nOpción no válida. Intente nuevamente.")
