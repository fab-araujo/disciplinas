from django.contrib import admin

# Register your models here.
from .models import Post, Comentario

admin.site.register(Post)
admin.site.register(Comentario)