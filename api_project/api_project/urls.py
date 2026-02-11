from django.urls import path, include
from rest_framework import DefaultRouters
from .views import BookViewSet

router = DefaultRouter()
router.register(r'book_all', view.BookViewSet, basename='book_all')
urlpatterns = router.urls
urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),
    path('api/', include('api.urls')),
]