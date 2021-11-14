from django.contrib import admin
from reviews.models import (Publisher, Contributor, Book, BookContributor, Review)


class BookAdmin(admin.ModelAdmin):
    list_display= ('title', 'isbn13')
    date_hierarchy= 'publication_date'
    list_filter= ('publisher','publication_date')
    search_fields= ('title','isbn')
    

class ContributorAdmin(admin.ModelAdmin):
    list_display = ('first_names','last_names','initialled_name',)
    search_fields = ('last_names__startswith','first_names')
    list_filter= ('last_names',)

admin.site.register(Publisher)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookContributor)
admin.site.register(Review)

