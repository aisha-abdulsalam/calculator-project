from django.urls import path
from .views import SimpleMathsCalc, CalculationHistory

urlpatterns = [
    path('calc/', SimpleMathsCalc.as_view(), name='calc'),
    path('history/', CalculationHistory.as_view(), name='history'),
]
 