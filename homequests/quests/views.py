from django.db.utils import IntegrityError
from quests.models import Alternativa, Quest, Tentativa
from quests.serializers import QuestSerializer, DisciplinaSerializer, QuestAlunoSerializer, TentativaSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from quests.models import Aluno

   
@api_view(http_method_names=['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def minhas_disciplinas(request):
    disciplinas = request.user.aluno.disciplina_set
    serializer =  DisciplinaSerializer(disciplinas, many=True)
    return Response(serializer.data)

@api_view(http_method_names=['POST'])
@authentication_classes([JSONWebTokenAuthentication])
def cadastro(request):
    try:
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
    except KeyError:
        return Response("Formato inválido")
    try:
        user = User.objects.create_user(username, email, password)
        aluno = Aluno(user=user, nome=username)
        user.save()
        aluno.save()
    except IntegrityError:
        return Response("Username já cadastrado")
    return Response(200)

@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(http_method_names=['GET'])
def quest(request, pk):
    quest = Quest.objects.get(id=pk)
    serializer = QuestAlunoSerializer(quest)
    return Response(serializer.data)

@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(http_method_names=['GET'])
def tentativas(request, pk):
    if request.user.is_superuser:
        quest = Quest.objects.get(id=pk)
        tentativas = Tentativa.objects.all().filter(quest=quest)
        serializer = TentativaSerializer(tentativas, many=True)
        return Response(serializer.data)
    else:
        return Response(401)

@authentication_classes([JSONWebTokenAuthentication])
@api_view(http_method_names=['POST'])
def enviar_tentativa(request):
    resposta_quest = request.data
    acertos = 0
    for key, resposta in resposta_quest["respostas"].items():
        alternativa = Alternativa.objects.get(id=int(resposta["alternativa"]))
        if alternativa.certa and alternativa.pergunta.id == int(resposta["pergunta"]):
            acertos += 1
    tentativa = Tentativa(quest=Quest.objects.get(id=resposta_quest["quest"]), aluno=Aluno.objects.get(id=request.user.aluno.id), pontos=acertos)
    tentativa.save()
    return Response({"msg": "Tentativa enviada com sucesso.", "nota": str(acertos)})

