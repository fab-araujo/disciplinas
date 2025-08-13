from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse

from .models import Pergunta, Escolha

from django.contrib import messages

def index(request):
    perguntas = Pergunta.objects.all()
    context = {
        'perguntas_template': perguntas
    }
    return render(request, 'index.html', context)

def detalhe(request, id_questao):
    pergunta = Pergunta.objects.get(id=id_questao)
    opcoes = Escolha.objects.filter(pergunta=id_questao)
    context = {
        'pergunta_tempalte':pergunta,
        'opcoes_template':opcoes
    }
    return render(request, 'detalhe.html', context)

def resultado(request, id_questao):
    pergunta = Pergunta.objects.get(id=id_questao)
    opcoes = Escolha.objects.filter(pergunta=id_questao)
    context = {
        'pergunta_tempalte':pergunta,
        'opcoes_template':opcoes
    }
    return render(request, 'resultado.html', context)

def votar(request, id_questao):
    if request.method == 'POST':
        post = request.POST
        escolha_votada = Escolha.objects.get(id = post['voto'])
        escolha_votada.votos = escolha_votada.votos + 1
        escolha_votada.save()
        messages.success(request, 'Voto computado com sucesso.')
        return redirect("index")

    pergunta = Pergunta.objects.get(id=id_questao)
    opcoes = Escolha.objects.filter(pergunta=id_questao)
    context = {
        'pergunta_tempalte':pergunta,
        'opcoes_template':opcoes
    }
    return render(request, 'votar.html', context)