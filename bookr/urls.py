from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from reviews.views import book_search
from bookr.views import profile

urlpatterns = [
    path('admin/', admin.site.urls),

    path('books/',include('reviews.urls')),
    path('',TemplateView.as_view(template_name="base.html")),
    path('book-search/', book_search, name='book-search'),

    path('accounts/',include(('django.contrib.auth.urls','auth'),('accounts'))),
    path('accounts/profile/', profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)