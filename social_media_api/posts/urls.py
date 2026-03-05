from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    # Feed endpoint
    path('feed/', views.FeedView.as_view(), name='feed'),
     path('<int:pk>/like/', views.PostLikeView.as_view(), name='post-like'),
    path('<int:pk>/unlike/', views.PostUnlikeView.as_view(), name='post-unlike'),

]