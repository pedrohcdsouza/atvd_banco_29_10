from rest_framework import serializers
from .models import Projeto, Tarefa


class TarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefa
        fields = "__all__"


class ProjetoBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projeto
        fields = ["id", "nome", "descricao"]


class ProjetoDetailSerializer(serializers.ModelSerializer):

    tarefas = serializers.SerializerMethodField()

    def get_tarefas(self, obj):
        tarefas = obj.tarefas.all()
        return TarefaSerializer(tarefas, many=True).data

    class Meta:
        model = Projeto
        fields = "__all__"
