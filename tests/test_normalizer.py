
import json
import sys
import unittest
from pathlib import Path

# Permitir importar los módulos de src
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from normalizer import normalize_transaction
from validator import validate_transaction, validate_transactions


# Cargar las reglas y datos de prueba
with open(BASE_DIR / "config" / "rules.json", "r", encoding="utf-8") as file:
    RULES = json.load(file)

with open(BASE_DIR / "data" / "transactions.json", "r", encoding="utf-8") as file:
    TRANSACTIONS = json.load(file)


class TestNormalizer(unittest.TestCase):

    def test_normalize_source_1(self):
        result = normalize_transaction(TRANSACTIONS[0], RULES)

        self.assertEqual(result["id"], "tx_001")
        self.assertEqual(result["amount"], 100.5)
        self.assertEqual(result["currency"], "USD")
        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(result["source"], "source_1")

    def test_normalize_source_2(self):
        result = normalize_transaction(TRANSACTIONS[1], RULES)

        self.assertEqual(result["id"], "204")
        self.assertEqual(result["amount"], 100.5)
        self.assertEqual(result["currency"], "USD")
        self.assertEqual(result["source"], "source_2")

    def test_normalize_source_3(self):
        result = normalize_transaction(TRANSACTIONS[2], RULES)

        self.assertEqual(result["id"], "A-77")
        self.assertEqual(result["amount"], 99.99)
        self.assertEqual(result["currency"], "EUR")
        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(result["source"], "source_3")

    def test_normalize_date_format(self):
        result = normalize_transaction(TRANSACTIONS[0], RULES)

        self.assertEqual(
            result["timestamp"],
            "2025-03-10T14:22:00Z"
        )

    def test_unsupported_currency(self):
        transaction = TRANSACTIONS[0].copy()
        transaction["currency"] = "GBP"

        with self.assertRaises(ValueError):
            normalize_transaction(transaction, RULES)

    def test_invalid_date(self):
        transaction = TRANSACTIONS[0].copy()
        transaction["timestamp"] = "fecha incorrecta"

        with self.assertRaises(ValueError):
            normalize_transaction(transaction, RULES)


class TestValidator(unittest.TestCase):

    def setUp(self):
        self.valid_transaction = normalize_transaction(
            TRANSACTIONS[0], RULES
        )

    def test_valid_transaction(self):
        errors = validate_transaction(
            self.valid_transaction, RULES
        )

        self.assertEqual(errors, [])

    def test_negative_amount(self):
        transaction = self.valid_transaction.copy()
        transaction["amount"] = -25.00

        errors = validate_transaction(transaction, RULES)

        self.assertTrue(
            any("mayor que cero" in error for error in errors)
        )

    def test_empty_identifier(self):
        transaction = self.valid_transaction.copy()
        transaction["id"] = ""

        errors = validate_transaction(transaction, RULES)

        self.assertTrue(
            any("identificador" in error.lower() for error in errors)
        )

    def test_invalid_status(self):
        transaction = self.valid_transaction.copy()
        transaction["status"] = "REFUNDED"

        errors = validate_transaction(transaction, RULES)

        self.assertTrue(
            any("estado" in error.lower() for error in errors)
        )

    def test_separate_valid_and_invalid_transactions(self):
        invalid_transaction = self.valid_transaction.copy()
        invalid_transaction["amount"] = -10.00

        result = validate_transactions(
            [self.valid_transaction, invalid_transaction],
            RULES
        )

        self.assertEqual(len(result["valid"]), 1)
        self.assertEqual(len(result["invalid"]), 1)


if __name__ == "__main__":
    unittest.main()
