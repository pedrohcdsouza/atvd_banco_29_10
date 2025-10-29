from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from usuario.views import UsuarioCadastroView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("cadastro/", UsuarioCadastroView.as_view({"post": "create"}), name="cadastro"),
]