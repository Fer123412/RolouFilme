from django.contrib.auth import views as auth_views
from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),

    path("filmes/", views.lista_filmes, name="filmes"),
    path("filmes/<int:movie_id>/", views.filme_detalhes, name="filme_detalhe"),
    path("filmes/<int:movie_id>/review/", views.criar_review, name="criar_review"),
    path("reviews/<int:review_id>/comentar/", views.comentar, name="comentar"),

    path("filmes/<int:movie_id>/comentar/", views.comentar_filme, name="comentar_filme"),
    path("comentarios/<int:comentario_id>/curtir/", views.curtir_comentario, name="curtir_comentario"),

    path("cadastro/", views.cadastro, name="cadastro"),
    path("login/", auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name='logout')
]