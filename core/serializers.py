from rest_framework import serializers
from .models import Account, Category, Transaction

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "nome", "moeda", "criado_em", "atualizado_em"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "nome", "tipo", "criado_em", "atualizado_em"]

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id", "tipo", "valor", "data", "descricao",
            "account", "category", "criado_em", "atualizado_em"
        ]

    def validate(self, attrs):
        category = attrs.get("category") or getattr(self.instance, "category", None)
        tipo = attrs.get("tipo") or getattr(self.instance, "tipo", None)
        valor = attrs.get("valor") or getattr(self.instance, "valor", None)

        if valor is not None and valor <= 0:
            raise serializers.ValidationError({"valor": "deve ser > 0"})
        if category and tipo and category.tipo != tipo:
            raise serializers.ValidationError({"tipo": "difere do tipo da categoria"})
        return attrs
