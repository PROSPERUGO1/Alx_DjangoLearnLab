from django.urls import path
from .views import *

urlpatterns = [
    path('books/', BookListView.as_view(), name='list_books'),
    path('books/create', BookCreateView.as_view(), name='create_books'),
    path('books/<int:pk>', BookDetailView.as_view(), name='book_detail'),
    path('books/update/<int:pk>', BookUpdateView.as_view(), name='book_update'),
    path('books/delete/<int:pk>', BookDeleteView.as_view(), name='book_delete'),
]