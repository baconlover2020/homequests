from dataclasses import field
from rest_framework import serializers
from quests.models import Aluno, Disciplina, Quest, Pergunta, Alternativa, Resposta, Tentativa, RespostaQuest
from random import shuffle

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ['user', 'nome']

class PerguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pergunta
        fields = ['id', 'quest','pergunta']

class AlternativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternativa
        fields = ['alternativa', 'pergunta']

class DisciplinaSerializer(serializers.ModelSerializer):
    # alunos = AlunoSerializer(many=True)
    class Meta:
        model = Disciplina
        fields = ['nome', 'turma']

class PerguntaQuestSerializer(serializers.ModelSerializer):
    alternativas = serializers.SerializerMethodField()
    # Esse metodo de aleatorizar alternativas poderia ser otimizado
    def get_alternativas(self, disciplina):
        alternativas_obj = Alternativa.objects.all()
        serializer = AlternativaSerializer(instance=alternativas_obj, many=True)
        a = list(serializer.data)
        shuffle(a)
        return a
    class Meta:
        model = Pergunta
        fields = ['pergunta', 'alternativas']

class QuestSerializer(serializers.ModelSerializer):
    disciplina = DisciplinaSerializer()
    perguntas = PerguntaQuestSerializer(source='pergunta_set', many=True)
    class Meta:
        model = Quest
        fields = ['nome', 'disciplina', 'perguntas']

class QuestAlunoSerializer(serializers.ModelSerializer):
    disciplina = serializers.StringRelatedField()
    perguntas = PerguntaQuestSerializer(source='pergunta_set', many=True)
    class Meta:
        model = Quest
        fields = ['nome', 'disciplina', 'pontos', 'prazo', 'tentativas', "perguntas"]

class TentativaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tentativa
        fields = ["quest", "aluno", "pontos"]

class DisciplinaParaAlunoSerializer(serializers.ModelSerializer):
    quests = serializers.SerializerMethodField()
    def get_quests(self, disciplina):
        visiveis = Quest.objects.all().filter(visivel=True) 
        serializer = QuestAlunoSerializer(instance=visiveis, many=True)
        if "perguntas" in serializer.data:
            serializer.data["perguntas"] = None
        return serializer.data
    class Meta:
        model = Disciplina
        fields = ['nome', 'turma', 'quests']
        depth = 0

class RespostaSerializer(serializers.ModelSerializer):
    pergunta = serializers.PrimaryKeyRelatedField(read_only=True)
    alternativa = serializers.PrimaryKeyRelatedField(read_only=True)
    aluno = serializers.PrimaryKeyRelatedField(read_only=True)
    resposta_quest = serializers.PrimaryKeyRelatedField(read_only=True) 
    class Meta:
        model = Resposta
        fields = '__all__'

class RespostaQuestSerializer(serializers.ModelSerializer):
    quest = serializers.PrimaryKeyRelatedField(read_only=True)
    aluno = serializers.PrimaryKeyRelatedField(read_only=True)
    respostas = RespostaSerializer()
    class Meta:
        model = RespostaQuest
        fields =  '__all__'


