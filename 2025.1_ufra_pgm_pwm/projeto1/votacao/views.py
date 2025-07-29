from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    context = {
        'mensagem': 'Bem-vindo à página INDEX!'
    }
    return render(request, 'index.html', context)

def detalhe(request, id_questao):
    context = {
        'mensagem': 'Bem-vindo à página DETALHE!'
    }
    return render(request, 'detalhe.html', context)

def votar(request, id_questao):
    context = {
        'mensagem': 'Bem-vindo à página VOTAR!'
    }
    return render(request, 'votar.html', context)

def resultado(request, id_questao):
    context = {
        'mensagem': 'Bem-vindo à página RESULTADO!'
    }
    return render(request, 'resultado.html', context)

