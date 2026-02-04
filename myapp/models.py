from django.db import models
from django.contrib.auth.models import User

class Calculation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num1 = models.FloatField()
    num2 = models.FloatField()
    operator = models.CharField(max_length=1)
    result = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.num1} {self.operator} {self.num2} = {self.result}"
