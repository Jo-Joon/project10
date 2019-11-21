from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_POST  # post 요청만 받아준다..
from .models import Movie, Review
from .forms import MovieForm, ReviewForm

def index(request):
    movies = Movie.objects.all()
    context = {'movies': movies,}
    return render(request, 'movies/index.html', context)


def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.review_set.all()
    person = get_object_or_404(get_user_model(), pk=request.user.id)
    review_form = ReviewForm()
    context = {'movie': movie, 'reviews':reviews, 'review_form':review_form, 'person': person,}
    return render(request, 'movies/detail.html', context)

@require_POST
def review_create(request, movie_pk):
    if request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.movie_id = movie_pk
            review.user = request.user
            review.save()
        return redirect('movies:detail', movie_pk)


@require_POST
def review_delete(request, movie_pk, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        if request.user == review.user:
            review.delete()
        return redirect('movies:detail', movie_pk)
    
    return HttpResponse('You are Unauthorized', status=401)

@login_required
def like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.like_users.filter(pk=request.user.pk).exists():
        movie.like_users.remove(request.user)
    else:
        movie.like_users.add(request.user)
    return redirect('movies:index')   


@login_required
def follow(request, movie_pk, user_pk):  # movie_pk 인자만 받아옴...
    # 게시글 유저(작성자)
    person = get_object_or_404(get_user_model(), pk=user_pk)
    # 접속 유저(로그인)
    user = request.user
    if person != user:  # 작성자와 로그인한 사람이 달라야 한다!
        # 내가(request.user) 게시글 유저(person.user) 팔로워 목록에 이미 존재한다면,
        # if user in person.followers.all(): 동일한 기능을 함.
        if person.followers.filter(pk=user.pk).exists():
            person.followers.remove(user)
        else:
            person.followers.add(user)
    return redirect('movies:detail', movie_pk)