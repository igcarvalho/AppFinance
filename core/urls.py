from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountView, CategoryView, TransactionView, summary
from django.http import JsonResponse

def healthcheck(_):
    return JsonResponse({"status": "ok"})

router = DefaultRouter()
router.register("accounts", AccountView, basename="account")
router.register("categories", CategoryView, basename="category")
router.register("transactions", TransactionView, basename="transaction")

urlpatterns = [
    path("health/", healthcheck),
    path("", include(router.urls)),
    path("summary/", summary),
]
