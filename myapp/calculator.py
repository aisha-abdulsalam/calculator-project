
from decimal import Decimal, getcontext
#from decimal import maths

# Prevent floating point precision issues
getcontext().prec = 28


class CalculatorService:

    # ---- BASIC OPS (multiple operands) ----
    @staticmethod
    def add(numbers):
        result = Decimal("0")
        for n in numbers:
            result += n
        return result

    @staticmethod
    def subtract(numbers):
        result = numbers[0]
        for n in numbers[1:]:
            result -= n
        return result

    @staticmethod
    def multiply(numbers):
        result = Decimal("1")
        for n in numbers:
            result *= n
        return result

    @staticmethod
    def divide(numbers):
        result = numbers[0]
        for n in numbers[1:]:
            if n == 0:
                raise ValueError("Division by zero")
            result /= n
        return result

    # ---- SCIENTIFIC OPS ----
    @staticmethod
    def power(base, exponent):
        return base ** exponent

    @staticmethod
    def sqrt(number):
        if number < 0:
            raise ValueError("Cannot calculate square root of a negative number")
        return number.sqrt()

    @staticmethod
    def modulo(a, b):
        if b == 0:
            raise ValueError("Modulo by zero")
        return a % b
