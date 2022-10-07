from django.shortcuts import render, redirect
from .models import Movie
from .forms import MovieForm

# Create your views here.
def index(request):
    movies = Movie.objects.order_by("-pk")

    context = {"movies": movies}

    return render(request, "movies/index.html", context)


def create(request):
    if request.method == "POST":
        movie_form = MovieForm(request.POST)
        if movie_form.is_valid():
            movie_form.save()
            return redirect("movies:index")
    else:
        movie_form = MovieForm()
    context = {"movie_form": movie_form}
    return render(request, "movies/create.html", context=context)


def detail(request, pk):

    movie = Movie.objects.get(pk=pk)

    context = {
        "movie": movie,
    }
    return render(request, "movies/detail.html", context)


def update(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.method == "POST":
        movie_form = MovieForm(request.POST, instance=movie)
        if movie_form.is_valid():
            movie_form.save()
            return redirect("movies:detail")
    else:
        movie_form = MovieForm(instance=movie)
    context = {"movie_form": movie_form}
    return render(request, "movies/update.html", context=context)


def delete(request, pk):
    movie = Movie.objects.get(pk=pk)
    movie.delete()

    return redirect("movies:index")


def main(request):
    return render(request, "movies/main.html")
