from django.urls import path

from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="blog/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="blog/logout.html"),
        name="logout",
    ),
    # Custom urls
    path("home/", views.Home.as_view(), name="home"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("profile/", views.profile, name="profile"),
    # 1. The Home Page (List of posts)
    path("", views.PostListView.as_view(), name="blog-home"),
    # 2. CRUD Paths
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/new/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
    # New Search & Tag Patterns
    path("search/", views.search, name="search"),
    path(
        "tags/<slug:tag_slug>/", views.PostByTagListView.as_view(), name="posts-by-tag"
    ),
    # Comments
    path(
        "post/<int:pk>/comments/new/",
        views.CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "comment/<int:pk>/update/",
        views.CommentUpdateView.as_view(),
        name="comment-update",
    ),
    path(
        "comment/<int:pk>/delete/",
        views.CommentDeleteView.as_view(),
        name="comment-delete",
    ),
]