# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Library

# Function-based view to list all books
def list_books(request):
    """
    Function-based view that lists all books in the database.
    """
    from .models import Book
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', books=books)

# Class-based view to display library details
class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_queryset(self):
        # Optimize query by prefetching related books and their authors
        return Library.objects.prefetch_related('books__author')

# Authentication Views

def register(request):
    """
    View for user registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('list_books')
    else:
        form = UserCreationForm()
    
    return render(request, 'relationship_app/register.html', {'form': form})

def login_view(request):
    """
    View for user login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('list_books')
    else:
        form = AuthenticationForm()
    
    return render(request, 'relationship_app/login.html', {'form': form})

@login_required
def logout_view(request):
    """
    View for user logout.
    """
    auth_logout(request)
    messages.info(request, 'You have been logged out.')
    return render(request, 'relationship_app/logout.html')