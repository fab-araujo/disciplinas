from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.index, name='index'),
    path('<int:id_questao>/detalhe', views.detalhe, name='detalhe'),
    path('<int:id_questao>/resultado', views.resultado, name='resultado'),
    path('<int:id_questao>/votar', views.votar, name='votar'),
]