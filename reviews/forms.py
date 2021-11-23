from django import forms
from .models import Publisher, Review, Book
class SearchForm(forms.Form):
    CHOICES =(('title','Title'),('contributor','Contributor'))
    search = forms.CharField(required=False, min_length=3)
    search_in = forms.ChoiceField(required=False, choices=CHOICES, initial='title')

class PublisherForm(forms.ModelForm):

    class Meta:
        model = Publisher
        fields = '__all__'


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(max_value=5, min_value= 0)

    class Meta:
        model = Review
        exclude = ('date_edited', 'book')


class BookMediaForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('cover','sample')