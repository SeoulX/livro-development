from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.land, name='land'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('aboutus_logged/', views.aboutus_logged, name='aboutus_logged'),
    path('profile/', views.profile, name='profile'),
    path('home/', views.home, name='home'),
    path('addbooks/', views.addbooks, name='addbooks'),
    path('browse/', views.browse, name='browse'),
    path('manageprofile/', views.manageprofile, name='manageprofile'),
    path('manageprofile_writer/', views.manageprofile_writer, name='manageprofile_writer'),
    path('profile_writer/', views.profile_writer, name='profile_writer'),
    path('book//<str:title>/', views.bookinformation, name='bookinformation'),
    path('browse_reader/', views.browse_reader, name='browse_reader'),
    path('browse_writer/', views.browse_writer, name='browse_writer'),
    path('fantasy/', views.fantasy, name='fantasy'),
    path('updatebooks/', views.updatebooks, name='updatebooks'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('browse-content/', views.browse_content, name='browse_content'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)