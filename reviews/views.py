from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from django.core.exceptions import PermissionDenied


from PIL import Image

from .models import Book, Review, Contributor, Publisher
from .utils import average_rating
from .forms import PublisherForm, SearchForm, ReviewForm, BookMediaForm

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
    
    if request.user.is_authenticated:
        max_viewed_books_length = 10
        viewed_books = request.session.get('viewed_books',[])
        viewed_book = [book.id, book.title]
        
        if viewed_book in viewed_books:
            viewed_books.pop(viewed_books.index(viewed_book))

        viewed_books.insert(0, viewed_book)
        
        viewed_books = viewed_books[:max_viewed_books_length]
        request.session['viewed_books'] = viewed_books

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

        if request.user.is_authenticated:
            search_history = request.session.get('search_history',[])
            searching = [search_in , search_field]
            
            if searching in search_history:
                search_history.pop(search_history.index(searching))
            
            search_history.insert(0,searching)
            request.session['search_history'] = search_history
    
  



        
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

@login_required
def review_edit(request, book_pk, review_pk= None):
    book = get_object_or_404(Book, pk=book_pk)
    review = None
    if review_pk is not None:
        review = get_object_or_404(Review, pk=review_pk)
    
        user = request.user
        if not user.is_staff or review.creator.id != user.id:
            raise PermissionDenied


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

@login_required()
def book_media(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookMediaForm(request.POST or None, request.FILES or None, instance=book)
    instance = book

    if form.is_valid():
        
        if form.cleaned_data.get('cover'):
            form.save(False) 
            image = Image.open(form.cleaned_data.get('cover'))
            image.thumbnail = (300, 300)
            form.save()
            instance = book #form.cleaned_data.get('cover')
            messages.success(request, f"{book} updated succefully")
            return redirect('book:book_details', book.pk)
    
    context = {'form':form, 'instance':instance, 'is_file_upload':True}
    return render(request, 'reviews/instance-form.html', context)

    
# @permission_required('edit_publisher')

def is_staff_user(user):
    return user.is_staff

@user_passes_test(is_staff_user)
def publisher_edit(request, pk=None):
    pass


