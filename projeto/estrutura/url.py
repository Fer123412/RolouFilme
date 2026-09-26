from django.urls import path
from . import views

app_name = "paginas"

urlpatterns = [
    path("", views.tarefas_home),
    path("adicionar/", views.tarefas_adicionar, name="adicionar")
]