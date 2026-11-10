from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg
from django.urls import reverse
from .models import Movie, Review, Comentario, Curtir
from .forms import ReviewForm, ComentarioForm
from .tmdb import completar_detalhes
from django.core.paginator import Paginator

User = get_user_model()

def home(request):
    filmes = Movie.objects.order_by('-id')[:20]
    return render(request,'home.html', {'filmes': filmes})

def lista_filmes(request):
    filmes = Movie.objects.order_by('titulo')
    return render(request, 'lista_filmes.html', {'filmes': filmes})

def filme_detalhes(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    try:
        completar_detalhes(movie)
    except Exception:
        pass #se o TMDB falhar, mostra o que ja tem

    reviews = (
        movie.reviews.select_related("user")
        .prefetch_related("comentarios__user")
        .order_by("-criado_em")
    )

    comentarios = (
        movie.comentarios.filter(parent_comentario__isnull=True)
        .select_related("user")
        .prefetch_related("respostas__user", "curtidas", "respostas__curtidas")
        .order_by("-criado_em")
    )

    media = reviews.aggregate(m=Avg("nota_review"))["m"]

    return render(request, "filme_detalhe.html", {
        "movie": movie,
        "reviews": reviews,
        "media": media,
        "review_form":ReviewForm(),
        "comentario_form": ComentarioForm(),
        "comentarios": comentarios
    })

def _voltar_aos_comentarios(movie_id):
    return redirect(reverse("filme_detalhe", args=[movie_id]) + "#comentarios")


@login_required
def criar_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
    return redirect("filme_detalhe", movie_id=movie.id)

@login_required
def comentar(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.user = request.user
            c.review = review
            c.save()

    return redirect("filme_detalhe", movie_id=review.movie_id)

@login_required
def comentar_filme(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.user = request.user
            c.movie = movie

            parent_id = request.POST.get("parent")
            if parent_id:
                parent = get_object_or_404(Comentario, id=parent_id, movie=movie)
                c.parent_comentario = parent.parent_comentario or parent
            c.save()
        return _voltar_aos_comentarios(movie_id)

@login_required
def curtir_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.method == "POST":
        curtida, criada = Curtir.objects.get_or_create(user=request.user, comentario=comentario)
        if not criada:
            curtida.delete()
    return _voltar_aos_comentarios(comentario.movie_id)


def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'cadastro.html', {'form': form})

def perfil(request, username):
    usuario = get_object_or_404(User, username=username)
    context = {
        "usuario": usuario,
        "total_seguidores": usuario.seguidores.count(),
        "total_seguindo": usuario.seguindo.count(),
        "reviews": usuario.reviews.select_related("movie").order_by("-criado_em"),
    }
    return render(request, "perfil.html", context)

def filmes(request):
    lista = Movie.objects.all()

    q = request.GET.get("q", "").strip()
    ano = request.GET.get("ano", "")
    ordem = request.GET.get("ordem", "titulo")

    if q:
        lista = lista.filter(titulo__icontains=q)
    if ano.isdigit():
        lista = lista.filter(ano=int(ano))

    ordens = {
        "titulo": "Título",
        "ano": "Ano",
        "-ano": "antigos",
        "antigos": "ano"
    }

    lista = lista.order_by(ordens.get(ordem, "titulo"))

    paginator = Paginator(lista, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    anos = Movie.objects.values_list("ano", flat=True).distinct().order_by("-ano")

    return render(
        request, "lista_filmes.html", {
            "page_obj": page_obj,
            "anos": anos,
            "ordens": ordens,
            "querystring": params.urlencode(),
        })