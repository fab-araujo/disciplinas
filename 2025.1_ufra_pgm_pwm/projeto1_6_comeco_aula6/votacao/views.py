from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Pergunta, Escolha

def index(request):
    perguntas = Pergunta.objects.all()
    context = {
        'perguntas_db': perguntas,
    }
    return render(request, 'index.html', context)

def detalhe(request, id_questao):
    pergunta = Pergunta.objects.get(id=id_questao)
    opcoes = Escolha.objects.filter(pergunta=pergunta)
    context = {
        'pergunta': pergunta,
        'opcoes': opcoes,
    }
    return render(request, 'detalhe.html', context)

def votar(request, id_questao):
    context = {
        'mensagem': 'Bem-vindo à página VOTAR!'
    }
    return render(request, 'votar.html', context)

def resultado(request, id_questao):
    pergunta = Pergunta.objects.get(id=id_questao)
    opcoes = Escolha.objects.filter(pergunta=pergunta)
    context = {
        'pergunta': pergunta,
        'opcoes': opcoes,
    }
    return render(request, 'resultado.html', context)

def sobre(request):
    context = {
        'mensagem': 'Bem-vindo à página SOBRE!'
    }
    return render(request, 'sobre.html', context)

