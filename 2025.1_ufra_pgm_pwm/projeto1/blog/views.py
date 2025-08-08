from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse

from .models import Post, Comentario

import datetime 

from django.contrib import messages

def index(request):
    posts = Post.objects.all()
    context = {
        'posts_template': posts
    }
    return render(request, 'index.html', context)

def detalhe(request, id_post):
    if request.method == 'POST':
        post = request.POST
        postagem = Post.objects.get(id=id_post)
        comentario = Comentario(post_id = postagem, texto = post['comentario'], com_date=datetime.datetime.now() )
        comentario.save()
        messages.success(request, 'Comentário adicionado com sucesso.')
        return redirect("index")
    post = Post.objects.get(id=id_post)
    comentarios = Comentario.objects.filter(post_id=id_post)
    context = {
        'post_template':post,
        'comentarios_template': comentarios
    }
    return render(request, 'detalhe.html', context)