from django.urls import path
from . import views
from .views import list_books, LibrayDetailView, LoginView, LogoutView, SignUpView, logout_confirm
#LibraryDetailView

app_name='rel_app'
# views.register
# add_book/
# edit_book/
# path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html), name='logout')
urlpatterns = [
    path('fbv/', list_books, name='fbv_details'),
    path('cbv/<int:pk>/', LibrayDetailView.as_view(), name='cbv_details'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', SignUpView.as_view(), name='register'),
    path('logout_confirm/', logout_confirm, name='logout_confirm'),
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
]