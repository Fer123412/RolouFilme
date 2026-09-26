from django.http import HttpResponse

def test_view(request):
    return HttpResponse("essa é a rota teste krl")

def index_view(request):
    return HttpResponse("<h1>Bem vindo!!!</h1>")
