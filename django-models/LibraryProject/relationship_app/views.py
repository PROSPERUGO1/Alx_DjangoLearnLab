from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# Function-based view to list all books
def list_books(request):
    """Function-based view that lists all books"""
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display library details
class LibraryDetailView(DetailView):
    """Class-based view that displays details for a specific library"""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        """Add extra context if needed"""
        context = super().get_context_data(**kwargs)
        # Library object is automatically available as 'library'
        return context