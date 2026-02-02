from django.urls import path
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Function-based view: List all books
    path('books/', views.list_books, name='list_books'),

    # Class-based view: Library details
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Optional: Add a library list view if needed
    # path('libraries/', views.LibraryListView.as_view(), name='library_list'),
]
