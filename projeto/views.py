from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from projeto.serializers import ProjetoBasicSerializer, ProjetoDetailSerializer, TarefaSerializer
from .models import Projeto, Tarefa

class ProjetoViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):

    queryset = Projeto.objects.all()
    serializer_class = ProjetoBasicSerializer

    @action(detail=True, methods=["get"], url_path="tarefas")
    def tarefas(self, request, pk=None):
        projeto = self.get_object()
        serializer = ProjetoDetailSerializer(projeto)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="criar-tarefa")
    def criar_tarefa(self, request, pk=None):
        projeto = self.get_object()
        tarefa_data = request.data

        tarefa = Tarefa.objects.create(
            nome=tarefa_data.get("nome"),
            descricao=tarefa_data.get("descricao"),
            projeto=projeto,
        )

        serializer = TarefaSerializer(tarefa)
        return Response(serializer.data)
