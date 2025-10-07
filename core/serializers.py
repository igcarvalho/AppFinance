# core/serializers.py
from jsonschema import ValidationError
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
            raise serializers.ValidationError("the transition value must be greater than 0")
        return valor
    
    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user if request else None

        account = attrs.get("account") or getattr(self.instance, "account", None)
        category = attrs.get("category") or getattr(self.instance, "category", None)
        tipo = attrs.get("tipo") or getattr(self.instance, "tipo", None)

        
        if category and tipo and category.tipo != tipo:
            raise serializers.ValidationError({"type": "differs from the category type "})

        
        if user:
            if account and account.user_id != user.id:
                raise serializers.ValidationError({"account": "does not belong to the user"})
            if category and category.user_id != user.id:
                raise serializers.ValidationError({"category": "does no belong to the user"})

        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
