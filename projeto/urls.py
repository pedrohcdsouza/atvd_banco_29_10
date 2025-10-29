from django.urls import include, path
from rest_framework.routers import DefaultRouter

from projeto.views import ProjetoViewset

router = DefaultRouter()
router.register(r"", ProjetoViewset, basename="projeto")

urlpatterns = [
    path("", include(router.urls)),
]
