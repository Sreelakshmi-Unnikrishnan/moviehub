from django import forms
from .models import Movie, Review,Category


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'poster', 'description', 'release_date', 'actors', 'category', 'trailer_link']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'actors': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'trailer_link': forms.URLInput(attrs={'class': 'form-control'}),
            
        }
        poster = forms.ImageField(required=False)
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.TextInput(attrs={'class': 'form-control'}),

        }
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']



