from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import filters
# from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
# from django_filters import rest_framework

# Create your views here.
class BookListView(generics.ListAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  
  filterset_fields = ['title', 'publication_year', 'author']
  search_fields = ['title', 'author__name']
  ordering_fields = ['title', 'publication_year']
  ordering = ['title'] 
  
  def get_queryset(self):
    queryset = Book.objects.all()
    year = self.request.query_params.get('year')
    author = self.request.query_params.get('author')
    title = self.request.query_params.get('title')

    if year:
        queryset = queryset.filter(publication_year=year)
    if author:
        queryset = queryset.filter(author=author)
    if title:
        queryset = queryset.filter(title=title)

    return queryset
  
class BookDetailView(generics.RetrieveAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  
class BookCreateView(generics.CreateAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
  
  def perform_create(self, serializer):
    serializer.save()

class BookUpdateView(generics.UpdateAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
  
  def perform_update(self, serializer):
    serializer.save()

class BookDeleteView(generics.DestroyAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]