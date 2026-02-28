from django.urls import path
from .views import RegisterView, CustomLoginView, UserProfileView, LogoutView, FollowUserView, UnfollowUserView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", CustomLoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("follow/<int:user_id>/", FollowUserView.as_view(), name="follow_user"),
    path("unfollow/<int:user_id>/", UnfollowUserView.as_view(), name="unfollow_user"),
]