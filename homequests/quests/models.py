from django.db import models
from django.contrib.auth.models import User

# Um aluno possui pode ser membro de multiplas disciplinas
# Uma disciplina pode ter multiplos alunos como membro
class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='aluno')
    nome = models.CharField(max_length=100)

class Disciplina(models.Model):
    nome = models.CharField(max_length=5)
    turma = models.IntegerField() 
    alunos = models.ManyToManyField(Aluno)

    def __str__(self):
        return self.nome

# Criação de uma "quest"
class Quest(models.Model):
    nome = models.TextField()
    disciplina = models.ForeignKey('Disciplina', on_delete=models.CASCADE)
    visivel = models.BooleanField(default=True)
    pontos = models.IntegerField()
    prazo = models.DateTimeField(null=True)
    tentativas = models.IntegerField()
    def __str__(self):
        return self.nome

# Objeto representando uma tentativa de completar uma quest
class Tentativa(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    pontos = models.IntegerField()


# Uma quest possui varias perguntas (One to many)
class Pergunta(models.Model):
    pergunta = models.TextField()
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    
# Uma pergunta possui varias alternativas (One to many)
class Alternativa(models.Model):
    alternativa = models.TextField()
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    certa = models.BooleanField(default=0)

class Resposta(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    alternativa = models.ForeignKey(Alternativa, on_delete=models.CASCADE)
    resposta_quest = models.ForeignKey('RespostaQuest', on_delete=models.CASCADE)

class RespostaQuest(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)