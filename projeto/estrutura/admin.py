from django.contrib import admin

# Register your models here.
from .models import (Movie,Review, Comentario, Curtir, Follow, ListaUsuario, Notificacao, Denuncia)

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Comentario)
admin.site.register(Curtir)
admin.site.register(Follow)
admin.site.register(ListaUsuario)
admin.site.register(Notificacao)
admin.site.register(Denuncia)
