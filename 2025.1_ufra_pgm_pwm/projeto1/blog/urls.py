from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id_post>/detalhe', views.detalhe, name='detalhe'),
]