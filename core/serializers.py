# core/serializers.py
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
        fields = ["id","tipo","valor","data","descricao","account","category","criado_em","atualizado_em"]

    def validate_valor(self, valor):
        if valor is None or valor <= 0:
            raise serializers.ValidationError("deve ser > 0")
        return valor

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user if request else None

        account = attrs.get("account") or getattr(self.instance, "account", None)
        category = attrs.get("category") or getattr(self.instance, "category", None)
        tipo = attrs.get("tipo") or getattr(self.instance, "tipo", None)

        # coerência com a categoria
        if category and tipo and category.tipo != tipo:
            raise serializers.ValidationError({"tipo": "difere do tipo da categoria"})

        # ownership
        if user:
            if account and account.user_id != user.id:
                raise serializers.ValidationError({"account": "não pertence ao usuário"})
            if category and category.user_id != user.id:
                raise serializers.ValidationError({"category": "não pertence ao usuário"})

        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
