from django.db import models

# Create your models here.
from uuid import uuid4

class Livro(models.Model):
    id_livro = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    ano_lancamento = models.IntegerField()
    estado = models.CharField(max_length=50)
    paginas = models.IntegerField()
    editora = models.CharField(max_length=100)
    dt_criacao = models.DateTimeField(auto_now_add=True)
    imagem = models.ImageField(upload_to='uploads/', null=True, blank=True)

    def __str__(self):
        return self.titulo