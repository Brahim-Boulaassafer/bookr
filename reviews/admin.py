from django.contrib import admin
from .models import Book, BookContributor, Review, Publisher, Contributor

admin.site.register(Book)
admin.site.register(BookContributor)
admin.site.register(Review)
admin.site.register(Publisher)
admin.site.register(Contributor)