from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

User = get_user_model()
# Create your views here.
@login_required
def index(request):
    index_users = User.objects.all()
    context = {'index_users':index_users,}
    return render(request, 'accounts/index.html', context)

def user_profile(request, user_pk):
    profile_user = get_object_or_404(User, pk=user_pk)
    user_reviews = profile_user.review_set.all()
    user_like_movies = profile_user.like_movies.all()
    context = {'profile_user':profile_user, 'user_reviews':user_reviews, 'user_like_movies':user_like_movies,}
    return render(request, 'accounts/profile.html', context)

def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')
    else:
        form = CustomUserCreationForm()
    context = {'form':form,}
    return render(request, 'accounts/auth_form.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'accounts:index')
    else:
        form = AuthenticationForm()
    context = {'form':form,}
    return render(request, 'accounts/auth_form.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts:index')

@login_required
def follow(request, user_pk):  
    person = get_object_or_404(get_user_model(), pk=user_pk)
    user = request.user
    if person != user:  
        if person.followers.filter(pk=user.id).exists():
            person.followers.remove(user)
        else:
            person.followers.add(user)
    return redirect('accounts:index')