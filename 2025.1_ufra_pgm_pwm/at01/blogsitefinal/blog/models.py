from django.db import models

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    imagem = models.ImageField(upload_to='post_images/', null=True, blank=True)

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    texto = models.CharField(max_length=300)
    com_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário em {self.post.titulo}"
