from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('books', views.books_page),
    path('logout', views.logout),
    path('create', views.create),
    path('books/<int:book_id>', views.check_if_edit_or_show),
    path('edit_book_page/<int:book_id>', views.edit_book_page),
    path('show_book_page/<int:book_id>', views.show_book_page),
    path('update', views.update),
    path('delete', views.delete),
    path('like_this_book/<int:book_id>', views.like_this_book),
    path('unlike/<int:book_id>', views.unlike),
]
