from django.db import models
from accounts.models import CustomUser

class SKUCHOICES(models.TextChoices):
    SP = ('sp', 'SP')
    MU = ('mu', 'MU')
    MO = ('mo', 'MO')
    TEL = ('te', 'TEL')
    OTHER = ('other', 'OTHER')


class Client(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="IR")

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=5, choices=SKUCHOICES.choices, default=SKUCHOICES.SP)

    def __str__(self):
        return self.name


class Sales(models.Model):
    doc_date = models.DateField(db_index=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.product.name} {self.quantity} {self.price} {self.value}'