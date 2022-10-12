from django.shortcuts import render, redirect
from .models import Movie
from .forms import MovieForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

# Create your views here.
def index(request):
    movies = Movie.objects.order_by("-pk")
    populars = Movie.objects.order_by("-hits")[:3]
    context = {
        "movies": movies,
        "populars": populars,
        }
    return render(request, "movies/index.html", context)


@login_required
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
    movie.hits += 1
    movie.save()
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
            return redirect("movies:detail", movie.pk)
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


def next(request, pk):
    movies = Movie.objects.order_by('-pk')
    movie = Movie.objects.get(pk=pk)
    pklist = []
    for m in movies:
        pklist.append(m.pk)
    nextpk = movie.pk
    small = min(pklist)
    while 1:
        nextpk -= 1
        # 1번 조건
        # nextpk가 1보다 작아지면
        if nextpk < small:
            return redirect("movies:detail", movie.pk)
        # 2번 조건
        # 지금 pk값에서 1을 빼서 만약에 있으면 값을 저장하고 종료
        elif nextpk in pklist:
            return redirect("movies:detail", nextpk)


def prev(request, pk):
    movies = Movie.objects.order_by('-pk')
    movie = Movie.objects.get(pk=pk)
    pklist = []
    for m in movies:
        pklist.append(m.pk)
    large = max(pklist)
    prevpk = movie.pk
    while 1:
        prevpk += 1
        # 1번 조건
        # 마지막 pk값보다 커지면 break
        if prevpk > large:
            return redirect("movies:detail", movie.pk)
        # 2번 조건
        # 지금 pk값에서 1을 더해서 만약에 있으면 값을 저장하고 종료
        elif prevpk in pklist:
            return redirect("movies:detail", prevpk)