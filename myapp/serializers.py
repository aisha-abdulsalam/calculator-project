from rest_framework import serializers
from .models import Calculation

class CalculationSerializer(serializers.Serializer):
    num1 = serializers.FloatField()
    num2 = serializers.FloatField()
    operator = serializers.ChoiceField(choices=['+', '-', '*', '/'])

