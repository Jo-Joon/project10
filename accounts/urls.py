from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_pk>/', views.user_profile, name='profile'),
]
