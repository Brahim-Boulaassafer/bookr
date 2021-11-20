from django.shortcuts import render, get_object_or_404
from .models import Book, Review, Contributor
from .utils import average_rating
from .forms import SearchForm

def book_list(request):
    books = Book.objects.all()
    book_list = []

    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating= average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)

        else:
            book_rating = None
            number_of_reviews = 0
        

        book_list.append({'book':book,'book_rating':book_rating,'number_of_reviews':number_of_reviews})

    context = {'book_list':book_list}
    return render(request, 'reviews/book_list.html',context)


def book_details(request, id):
    book = get_object_or_404(Book, id= id)
    if book:
        reviews = book.review_set.all()
        book_rating= average_rating([review.rating for review in reviews])
    context = {'book':book, 'book_rating':book_rating, 'reviews': reviews}
    return render(request, 'reviews/book_details.html', context)

def book_search(request):
    form = SearchForm(request.GET or None)
    search_field = ''
    books = set()
    if form.is_valid():
        search_in = form.cleaned_data['search_in']
        search_field = form.cleaned_data['search']
        if search_in == 'title':
            books = Book.objects.filter(title__icontains= search_field)            
        else:
            fname_contributors = Contributor.objects.filter(first_names__icontains=search_field)
            for contributor in fname_contributors:
                for book in contributor.book_set.all():
                    books.add(book)
            
            lname_contributors = Contributor.objects.filter(last_names__icontains=search_field)
            for contributor in lname_contributors:
                for book in contributor.book_set.all():
                    books.add(book)

        
        
    context = {'form':form, 'book_list':books, 'search':search_field}
    return render(request, 'reviews/search-results.html',context)