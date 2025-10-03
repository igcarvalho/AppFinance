from rest_framework import viewsets, permissions, decorators, response
from django.db.models import Sum
from .models import Account, Category, Transaction
from .serializers import AccountSerializer, CategorySerializer, TransactionSerializer

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj, "user_id", None) == request.user.id

class BaseOwnedViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # cada ViewSet define self.queryset_base
        return self.queryset_base.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AccountView(BaseOwnedViewSet):
    queryset_base = Account.objects.all()
    serializer_class = AccountSerializer

class CategoryView(BaseOwnedViewSet):
    queryset_base = Category.objects.all()
    serializer_class = CategorySerializer

class TransactionView(BaseOwnedViewSet):
    queryset_base = Transaction.objects.select_related("account", "category")
    serializer_class = TransactionSerializer

# /summary/ simples (saldo e agregações)
@decorators.api_view(["GET"])
def summary(request):
    qs = Transaction.objects.filter(user=request.user)
    ano = request.query_params.get("ano")
    mes = request.query_params.get("mes")
    if ano: qs = qs.filter(data__year=ano)
    if mes: qs = qs.filter(data__month=mes)

    receitas = qs.filter(tipo="RECEITA").aggregate(total=Sum("valor"))["total"] or 0
    despesas = qs.filter(tipo="DESPESA").aggregate(total=Sum("valor"))["total"] or 0
    saldo = receitas - despesas

    por_categoria = (
        qs.values("category__nome")
          .annotate(total=Sum("valor"))
          .order_by("-total")
    )
    # resposta enxuta
    return response.Response({
        "saldo": float(saldo),
        "receitas": float(receitas),
        "despesas": float(despesas),
        "por_categoria": [
            {"categoria": r["category__nome"], "total": float(r["total"])} for r in por_categoria
        ],
    })
