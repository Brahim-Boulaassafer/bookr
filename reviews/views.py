from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Book, Review, Contributor, Publisher
from .utils import average_rating
from .forms import PublisherForm, SearchForm, ReviewForm

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


def publisher_edit(request, pk=None):
    publisher = None

    if pk is not None:
        publisher = get_object_or_404(Publisher, pk=pk)

    form = PublisherForm(request.POST or None, instance=publisher)
    if form.is_valid():
        updated_publisher = form.save()
        if updated_publisher is None:
            messages.success(request, f"Publisher ``{updated_publisher}`` was created.")
        else:
            messages.success(request, f"Publisher ``{updated_publisher}`` was updated.")
        return redirect('book:publisher_edit', updated_publisher.pk)
    
    return render(request, 'reviews/instance-form.html',{ 'form':form, 'instance':publisher, 'title':'Publisher'})


def review_edit(request, book_pk, review_pk= None):
    book = get_object_or_404(Book, pk=book_pk)
    review = None
    if review_pk is not None:
        review = get_object_or_404(Review, pk=review_pk)
    
    form = ReviewForm(request.POST or None, instance=review)
    if form.is_valid():
        updated_view = form.save(commit=False)
        updated_view.book = book
        updated_view.date_edited = timezone.now()
        form.save()
        if updated_view is None:
            messages.success(request, f'Review for "{book}" was created.')
        else:
            messages.success(request, f'Review for "{book}" was updated.')
        return redirect('book:book_details', book_pk)

    return render(request, 'reviews/instance-form.html', {'form':form, 'instance': book, 'title':'Review', 'instance_model':review})