from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your views here.
def index(request):
    index_users = User.objects.all()
    context = {'index_users':index_users,}
    return render(request, 'accounts/index.html', context)

def user_profile(request, user_pk):
    profile_user = get_object_or_404(User, pk=user_pk)
    user_reviews = profile_user.review_set.all()
    context = {'profile_user':profile_user, 'user_reviews':user_reviews,}
    return render(request, 'accounts/profile.html', context)

