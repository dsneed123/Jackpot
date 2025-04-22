from django.db import models
from django.contrib.auth.models import User

class Bucket(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buckets')

    def __str__(self):
        return f"{self.name} - {self.percentage}%"
class Item(models.Model):
    name = models.CharField(max_length=100)
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE, related_name='items')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.quantity} in {self.bucket.name}"
