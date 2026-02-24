from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
class Profile(models.Model):
    # OneToOneField means: One User has exactly One Profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The extra fields we want
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} Profile"

    def get_absolute_url(self):
        # This tells Django: "If you want to view this post, go to the 'post-detail' view"
        return reverse("profile")

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )

    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # This tells Django: "If you want to view this post, go to the 'post-detail' view"
        return reverse("post-detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.content[:20]}"

    # This sends the user back to the POST they commented on, not the comment itself
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.post.pk})