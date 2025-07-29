from django.contrib import admin

# Register your models here.
from .models import Pergunta, Escolha

admin.site.register(Pergunta)
admin.site.register(Escolha)