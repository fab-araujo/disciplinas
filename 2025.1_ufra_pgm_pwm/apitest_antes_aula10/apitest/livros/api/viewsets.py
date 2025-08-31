from rest_framework import viewsets
from livros.api import serializers
from livros import models

class LivrosViewSet(viewsets.ModelViewSet):
    queryset = models.Livro.objects.all()
    serializer_class = serializers.LivroSerializer