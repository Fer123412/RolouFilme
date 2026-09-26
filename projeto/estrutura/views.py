from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def tarefas_home(request):
    contexto = {
        "nome":"Lan"
    }
    return render(request,'telas/login.html', contexto)

def tarefas_adicionar(request):
    return HttpResponse("tarefas adicionaiss")