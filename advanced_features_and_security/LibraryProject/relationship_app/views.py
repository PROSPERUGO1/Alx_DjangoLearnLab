from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.urls import reverse_lazy
from .models import Library, Book
# from django.contrib.auth.decorators import permission_required

# Create your views here.
def list_books(request):
  books = Book.objects.all()
  template = 'relationship_app/list_books.html'
  return render(request, template, {'books':books})

class LibrayDetailView(DetailView):
  model = Library
  template_name = 'relationship_app/library_detail.html'
  
class LoginView(LoginView):
  pass

class LogoutView(LogoutView):
  template_name = 'relationship_app/logout.html'
  
class SignUpView(CreateView):
  # UserCreationForm()
  form_class = UserCreationForm
  success_url = reverse_lazy('login')
  template_name = 'relationship_app/register.html'

def logout_confirm(request):
  return render(request, 'relationship_app/logout.html', {})

def is_admin(user):
    return user.userprofile.role == 'admin'

def is_librarian(user):
    return user.userprofile.role == 'librarian'

def is_member(user):
    return user.userprofile.role == 'member'
  
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        Book.objects.create(title=title)
        return redirect('book_list')

    return render(request, 'relationship_app/add_book.html')
  
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.save()
        return redirect('book_list')

    return render(request, 'relationship_app/edit_book.html', {'book': book})
  
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.delete()
        return redirect('book_list')

    return render(request, 'relationship_app/delete_book.html', {'book': book})