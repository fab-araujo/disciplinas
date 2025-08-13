from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('detalhe/<int:id_questao>', views.detalhe, name='detalhe'),
    path('votar/<int:id_questao>', views.votar, name='votar'),
    path('resultado/<int:id_questao>', views.resultado, name='resultado'),
]
