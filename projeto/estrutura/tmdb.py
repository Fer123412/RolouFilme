import requests
from django.conf import settings
from .models import Movie

BASE = 'https://api.themoviedb.org/3'
IMG = 'https://image.tmdb.org/t/p/w500'

def _get(path, **params):
    params.setdefault("language", "pt-BR")
    r = requests.get(
        f"{BASE}{path}", 
        params=params, 
        headers={"Authorization": f"Bearer {settings.TMBD_TOKEN}"},
        timeout=10,
        )

    r.raise_for_status()
    return r.json()

def _ano(data):
    return int(data[:4]) if data else 0

def sincronizar_populares():
    """Sincroniza os filmes populares do TMDB com o banco de dados local.
    """
    filmes = []
    for item in _get("/movie/popular")["results"]:
        movie, _= Movie.objects.update_or_create(
            tmdb_id = item["id"],
            defaults = {
                "titulo": item["title"],
                "ano": _ano(item.get("release_date")),
                "sinopse": item.get("overview") or "Sem sinopse disponivel.",
                "poster_url": IMG + item["poster_path"] if item.get("poster_path") else None,
            },
        )
        filmes.append(movie)
    return filmes

def completar_detalhes(movie):
    """
    Preenche diretor e duração (só vem no endpoint de detalhes).
    """

    if movie.diretor and movie.duracao:
        return movie

    d = _get(f"/movie/{movie.tmbd_id}", append_to_response="credits")
    diretor = next(
        (p["name"] for p in d["credits"]["crew"] if p["job"] == "Director"), ""
    )

    movie.diretor = diretor
    movie.duracao = d.get("runtime")
    movie.save()
    return movie