from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from .serializers import UsuarioCadastroSerializer

class UsuarioCadastroView(mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioCadastroSerializer
    