# core/models.py
from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q, CheckConstraint, UniqueConstraint

class TimeStamped(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Account(TimeStamped):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    moeda = models.CharField(max_length=10, default="BRL")

    class Meta:
        constraints = [
            # nome da conta único por usuário
            UniqueConstraint(fields=["user", "nome"], name="uniq_account_nome_per_user"),
        ]

class Category(TimeStamped):
    TIPO = (("DESPESA", "DESPESA"), ("RECEITA", "RECEITA"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=7, choices=TIPO)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "nome", "tipo"], name="uniq_category_nome_tipo_per_user"),
        ]

class Transaction(TimeStamped):
    TIPO = Category.TIPO
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=7, choices=TIPO)
    valor = models.DecimalField(max_digits=12, decimal_places=2,
                                validators=[MinValueValidator(Decimal("0.01"))])
    data = models.DateField()
    descricao = models.TextField(blank=True, default="")

    def clean(self):
        # regra de coerência com a categoria
        if self.category and self.tipo != self.category.tipo:
            raise ValidationError({"tipo": "difere do tipo da categoria"})

    def save(self, *args, **kwargs):
        # garante que validators + clean() rodam sempre
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(valor__gt=0), name="transaction_valor_gt_zero"),
        ]
