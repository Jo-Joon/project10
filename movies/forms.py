from django import forms
from django.forms import ModelForm
from .models import Movie, Review


class MovieForm(forms.ModelForm):
    
    class Meta:
        model = Movie
        fields = ('title', 'audience', 'poster_url', 'description')

class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ('content', 'score')

