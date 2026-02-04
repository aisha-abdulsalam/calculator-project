from decimal import Decimal
from django.test import TestCase
from myapp.calculator import CalculatorService

class CalculatorServiceTests(TestCase):

    def test_add(self):
        numbers = [Decimal("1.1"), Decimal("2.2"), Decimal("3.3")]
        result = CalculatorService.add(numbers)
        self.assertEqual(result, Decimal("6.6"))

    def test_subtract(self):
        numbers = [Decimal("10"), Decimal("3"), Decimal("2")]
        result = CalculatorService.subtract(numbers)
        self.assertEqual(result, Decimal("5"))

    def test_multiply(self):
        numbers = [Decimal("2"), Decimal("3"), Decimal("4")]
        result = CalculatorService.multiply(numbers)
        self.assertEqual(result, Decimal("24"))

    def test_divide(self):
        result = CalculatorService.divide(Decimal("10"), Decimal("2"))
        self.assertEqual(result, Decimal("5"))
        # Check division by zero raises
        with self.assertRaises(ZeroDivisionError):
            CalculatorService.divide(Decimal("10"), Decimal("0"))

    def test_power(self):
        result = CalculatorService.power(Decimal("2"), Decimal("3"))
        self.assertEqual(result, Decimal("8"))

    def test_sqrt(self):
        result = CalculatorService.sqrt(Decimal("16"))
        self.assertEqual(result, Decimal("4"))

    def test_modulo(self):
        result = CalculatorService.modulo(Decimal("10"), Decimal("3"))
        self.assertEqual(result, Decimal("1"))


