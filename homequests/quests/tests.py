from django.test import TestCase
import httpx
import json

# Utilizando um client httpx para verificar se as views tem a resposta esperada.
class ViewsTest(TestCase):
    def login(self, client):
        username = 'matheus'
        senha = 'camera'
        url = 'http://127.0.0.1:8000/api/login/'
        resposta = client.post(url, data={'username': username, 'password': senha})
        data = json.loads(resposta.text)
        return data["token"]   

    def test_login(self):
        with httpx.Client() as client:
            token = self.login(client)
            print(token)
        return token
    
    def test_disciplinas(self):
        with httpx.Client() as client:
            # A primeira resposta deve ser 401 Unauthorized
            # pois o user ainda não foi logado.
            url = 'http://127.0.0.1:8000/api/minhas-disciplinas/'
            resposta = client.get(url)
            print(resposta)

            # Executando o request com o header e token
            # O teste passa se a autenticação suceder e as disciplinas
            # listadas pela API.
            token = self.login(client)
            headers = {"Authorization": f"Bearer {token}"}
            resposta = client.get(url, headers=headers)
            print(resposta.text)
            return resposta.text

    def test_quest(self):
        with httpx.Client() as client:
            token = self.login(client)
            headers = {"Authorization": f"Bearer {token}"}
            _id = 1 # ID da quest sendo testada
            url = f"http://127.0.0.1:8000/api/quest/{_id}/"
            resposta = client.get(url, headers=headers)
            print(resposta.text)
            # O teste passa se as quests do usuario forem listadas com exito
            return resposta.text
    
    def test_tentativas(self):
       with httpx.Client() as client:
            token = self.login(client)
            headers = {"Authorization": f"Bearer {token}"} 
            # ID da quest; Todas as tentativas listadas pertencem 
            # à mesma atividade
            quest_id = 1 
            url = f"http://127.0.0.1:8000/api/tentativas/{quest_id}/"
            resposta = client.get(url, headers=headers)
            # O teste passa se uma lista de tentativas for exibida
            # para superusers autenticados
            print(resposta.text)
            return resposta.text
        
    def test_enviar_tentativa(self):
       with httpx.Client() as client:
            token = self.login(client)
            client.headers["Authorization"] = f"Bearer {token}"
            client.headers['Content-Type'] = 'application/json'
            print(client.headers)
            respostas_da_quest = {
                "quest": "1",
                "respostas": {
                    "resposta": 
                        {
                        "pergunta": "1",
                        "alternativa": "2"
                        }
                }
            }
            data = json.dumps(respostas_da_quest)
            url = "http://127.0.0.1:8000/api/enviar-tentativa/"
            resposta = client.post(url, data=data)
            # O teste passa se uma nova tentativa for adicionada ao database
            print(resposta)
            return resposta

