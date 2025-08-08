from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Pergunta, Escolha
from django.contrib import messages

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
    if request.method == 'POST':
        pergunta = Pergunta.objects.get(id=id_questao)
        voto_id = request.POST.get('opcao')
        opcao = Escolha.objects.get(id=voto_id)
        opcao.votos += 1
        opcao.save()
        messages.success(request, 'Voto registrado com sucesso!')
        return redirect('resultado', id_questao=id_questao)

    pergunta = Pergunta.objects.get(id=id_questao)
    opcoes = Escolha.objects.filter(pergunta=pergunta)
    context = {
        'pergunta': pergunta,
        'opcoes': opcoes,
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

