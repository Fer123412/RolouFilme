from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL


class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    titulo = models.CharField(max_length=200)
    ano = models.IntegerField()
    sinopse = models.TextField()
    poster_url = models.CharField(max_length=255, blank=True, null=True)
    diretor = models.CharField(max_length=100, blank=True)
    duracao = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} ({self.ano})"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    nota_review = models.IntegerField()
    texto_review = models.TextField()
    contem_spoiler = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review de {self.user} sobre {self.movie}"


class Comentario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comentarios")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comentarios")
    parent_comentario = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="respostas")
    texto_comentario = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comentário de {self.user} em {self.review}"


class Curtir(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="curtidas")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, blank=True, null=True, related_name="curtidas")
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE, blank=True, null=True, related_name="curtidas")
    criado_em = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seguindo")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seguidores")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["follower", "followed"], name="unique_follow")
        ]


class ListaUsuario(models.Model):
    STATUS_CHOICES = [
        ("assistido", "Assistido"),
        ("quero_ver", "Quero ver"),
        ("favorito", "Favorito"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lista_filmes")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="na_lista_de")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    criado_em = models.DateTimeField(auto_now_add=True)


class Notificacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notificacoes")
    tipo = models.CharField(max_length=100)
    referencia_id = models.IntegerField()
    lida = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)


class Denuncia(models.Model):
    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("em_analise", "Em análise"),
        ("resolvida", "Resolvida"),
        ("rejeitada", "Rejeitada"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="denuncias")
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE, blank=True, null=True, related_name="denuncias")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, blank=True, null=True, related_name="denuncias")
    motivo = models.CharField(max_length=100)
    status_denuncia = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pendente")
    criado_em = models.DateTimeField(auto_now_add=True)