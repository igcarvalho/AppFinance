from django.contrib.auth import get_user_model
from rest_framework import decorators, permissions, response, status
from rest_framework.serializers import ModelSerializer, CharField, ValidationError
from core.models import Category
User = get_user_model()

class RegisterSerializer(ModelSerializer):
    password = CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ["username", "email", "password"]
    def create(self, data):
        if User.objects.filter(username=data["username"]).exists():
            raise ValidationError({"username": "already existed"})
        return User.objects.create_user(**data)

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def register(request):
    s = RegisterSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    user = s.save()
    defaults = [("Alimentação","DESPESA"),("Moradia","DESPESA"),("Transporte","DESPESA"),("Salário","RECEITA")]
    for nome,tipo in defaults:
        Category.objects.get_or_create(user=user, nome=nome, tipo=tipo)
    return response.Response({"id": user.id, "username": user.username}, status=status.HTTP_201_CREATED)




@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
def me(request):
    u = request.user
    return response.Response({"id": u.id, "username": u.username, "email": u.email})
