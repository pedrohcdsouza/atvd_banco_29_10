from django.db import models

class Projeto(models.Model):

    nome = models.CharField(max_length=255)
    dtainicio = models.DateTimeField(auto_now_add=True)
    dtaconclusao = models.DateTimeField(null=True, blank=True)
    descricao = models.TextField()

class Tarefa(models.Model):

    titulo = models.CharField(max_length=255)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='tarefas')
    concluida = models.BooleanField(default=False)
    dtainicio = models.DateTimeField(auto_now_add=True)
    dtaconclusao = models.DateTimeField(null=True, blank=True)
    prioridade = models.IntegerField()