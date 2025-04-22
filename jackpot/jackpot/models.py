from django.db import models
from django.contrib.auth.models import User

class Bucket(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buckets')

    def __str__(self):
        return f"{self.name} - {self.percentage}%"
