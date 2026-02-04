from decimal import Decimal
import logging

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle

#Rate limiting
from .models import Calculation
from .calculator import CalculatorService

class CalculationThrottle(UserRateThrottle):
    scope = "calc"


class SimpleMathsCalc(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [CalculationThrottle]   # LEVEL 7 (rate limit)

    def post(self, request):
        operator = request.data.get("operator")
        operands = request.data.get("operands")

        # LEVEL 5/6 VALIDATION
        if not operator or not operands:
            return Response({
                "success": False,
                "error": {
                    "code": "MISSING_PARAMETER",
                    "message": "operator and operands are required"
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        # LEVEL 6: DECIMAL
        try:
            numbers = [Decimal(str(n)) for n in operands]
        except Exception as e:
            logging.error(f"Invalid operands: {operands} | {str(e)}")  # LEVEL 7 LOGGING
            return Response({
                "success": False,
                "error": {
                    "code": "INVALID_OPERAND",
                    "message": "Operands must be numeric"
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        # LEVEL 5/6: OPERATOR WHITELIST 
        allowed_ops = ["+", "-", "*", "/", "pow", "sqrt", "mod"]

        if operator not in allowed_ops:
            logging.error(f"Invalid operator: {operator}")  # LEVEL 7 LOGGING
            return Response({
                "success": False,
                "error": {
                    "code": "INVALID_OPERATOR",
                    "message": "Operator not allowed"
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        # LEVEL 7: CACHING 
        cache_key = f"calc:{operator}:{operands}"
        cached_result = cache.get(cache_key)

        if cached_result:
            return Response({
                "success": True,
                "result": cached_result,
                "cached": True
            }, status=status.HTTP_200_OK)

        # LEVEL 6: SERVICES LAYER
        try:
            if operator == "+":
                result = CalculatorService.add(numbers)

            elif operator == "-":
                result = CalculatorService.subtract(numbers)

            elif operator == "*":
                result = CalculatorService.multiply(numbers)

            elif operator == "/":
                result = CalculatorService.divide(numbers)

            elif operator == "pow":
                result = CalculatorService.power(numbers[0], numbers[1])

            elif operator == "sqrt":
                result = CalculatorService.sqrt(numbers[0])

            elif operator == "mod":
                result = CalculatorService.modulo(numbers[0], numbers[1])

        except Exception as e:
            logging.error(f"Calculation error: {operator} {operands} | {str(e)}")  # LEVEL 7 LOGGING
            return Response({
                "success": False,
                "error": {
                    "code": "CALCULATION_ERROR",
                    "message": str(e)
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        # LEVEL 7: STORE IN CACHE (5 minutes)
        cache.set(cache_key, str(result), timeout=300)

        # LEVEL 3/4: SAVE TO DB 
        Calculation.objects.create(
            user=request.user,
            num1=float(numbers[0]),
            num2=float(numbers[1]) if len(numbers) > 1 else 0,
            operator=operator,
            result=float(result)
        )

        return Response({
            "success": True,
            "result": str(result),
            "cached": False
        }, status=status.HTTP_200_OK)


class CalculationHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        calculations = Calculation.objects.filter(
            user=request.user
        ).order_by("-timestamp")[:10]

        data = []
        for calc in calculations:
            data.append({
                "num1": calc.num1,
                "num2": calc.num2,
                "operator": calc.operator,
                "result": calc.result,
                "timestamp": calc.timestamp
            })

        return Response({
            "success": True,
            "data": data
        }, status=status.HTTP_200_OK)



