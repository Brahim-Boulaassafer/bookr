from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('',views.book_list,name= 'book_list'),
    path('<int:id>/',views.book_details,name= 'book_details'),
    path('publishers/<int:pk>/',views.publisher_edit,name= 'publisher_edit'),
    path('publishers/new/',views.publisher_edit,name= 'publisher_create'),
    path('<int:book_pk>/reviews/<int:review_pk>',views.review_edit,name= 'review_edit'),
    path('<int:book_pk>/reviews/new/',views.review_edit,name= 'review_create'),
]
