from django.urls import path
from . import views

app_name='movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/review_create', views.review_create, name='review_create'),
    path('<int:movie_pk>/review_delete/<int:review_pk>', views.review_delete, name='review_delete'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('<int:movie_pk>/follow/<int:user_pk>/', views.follow, name='follow'),
]
