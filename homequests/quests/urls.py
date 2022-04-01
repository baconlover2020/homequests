from django.urls import path
from quests import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('minhas-disciplinas/', views.minhas_disciplinas),
    path('quest/<int:pk>/', views.quest),
    path('login/', obtain_jwt_token),
    path('cadastro/', views.cadastro),
    path('tentativas/<int:pk>/', views.tentativas),
    path('enviar-tentativa/', views.enviar_tentativa)
]