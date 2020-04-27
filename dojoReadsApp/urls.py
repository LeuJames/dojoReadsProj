from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('books', views.books),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('books/add', views.addBook),
    path('submitBook', views.submitBook),
    path('books/<int:bookID>', views.bookPage),
    path('submitReview/<int:bookID>', views.submitReview),
    path('users/<int:userID>', views.userPage),
    path('delete/<int:reviewID>', views.deleteReview)
]