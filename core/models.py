# core/models.py
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

class TimeStamped(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Account(TimeStamped):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    moeda = models.CharField(max_length=10, default="BRL")

class Category(TimeStamped):
    TIPO = (("DESPESA", "DESPESA"), ("RECEITA", "RECEITA"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=7, choices=TIPO)

class Transaction(TimeStamped):
    TIPO = Category.TIPO
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=7, choices=TIPO)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField()
    descricao = models.TextField(blank=True, default="")
    def clean(self):
        if self.valor is None or self.valor <= 0:
            raise ValidationError("valor deve ser > 0")
        if self.category and self.tipo != self.category.tipo:
            raise ValidationError("tipo da transação difere do tipo da categoria")

