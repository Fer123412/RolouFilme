from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg

from .models import Movie, Review
from .forms import ReviewForm, ComentarioForm
from .tmdb import completar_detalhes
# Create your views here.


def home(request):
    filmes = Movie.objects.order_by('-id')[:12]
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

    media = reviews.aggregate(m=Avg("nota_review"))["m"]

    return render(request, "filme_detalhe.html", {
        "movie": movie,
        "reviews": reviews,
        "media": media,
        "review_form":ReviewForm(),
        "comentario_form": ComentarioForm(),
    })

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