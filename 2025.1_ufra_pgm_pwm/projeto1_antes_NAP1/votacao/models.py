from django.db import models

# Create your models here.
class Pergunta(models.Model):
    texto = models.CharField(max_length=200)
    data_pub = models.DateTimeField()
    imagem = models.ImageField(upload_to="uploads/", default="")

class Escolha(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    texto = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)