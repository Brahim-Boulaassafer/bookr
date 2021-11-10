from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('',views.book_list,name= 'book_list'),
    path('books/<int:id>/',views.book_details,name= 'book_details'),
]
