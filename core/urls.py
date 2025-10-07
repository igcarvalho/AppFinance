from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, CategoryViewSet, TransactionViewSet, summary
from django.http import JsonResponse

def healthcheck(_):
    return JsonResponse({"status": "ok"})

router = DefaultRouter()
router.register("accounts", AccountViewSet, basename="account")
router.register("categories", CategoryViewSet, basename="category")
router.register("transactions", TransactionViewSet, basename="transaction")

urlpatterns = [
    path("health/", healthcheck),
    path("", include(router.urls)),
    path("summary/", summary),
]
