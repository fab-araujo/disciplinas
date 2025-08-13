from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comentario
from .forms import ComentarioForm
from django.contrib import messages

def index(request):
    posts = Post.objects.all().order_by('-pub_date')
    return render(request, 'blog/index.html', {'posts': posts})

def detalhe_postagem(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comentarios = Comentario.objects.filter(post=post)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post
            comentario.save()
            messages.success(request, 'Comentário enviado com sucesso!')
            return redirect('index')
    else:
        form = ComentarioForm()

    return render(request, 'blog/detalhe.html', {
        'post': post,
        'comentarios': comentarios,
        'form': form
    })
