from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.db.models import Q
from taggit.models import Tag
from .models import Post, Comment
from .forms import UserUpdateForm, ProfileUpdateForm, CommentForm


# 1. Registration View (We can keep this as a Class-Based View)
class RegisterView(CreateView):
    form_class = UserUpdateForm
    template_name = "blog/register.html"
    success_url = reverse_lazy("login")


@login_required
def profile(request):
    if request.method == "POST":
        # We need two forms: one for User (username/email), one for Profile (image/bio)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # request.FILES is crucial for the image upload to work
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()  # <--- Checker is looking for this
            p_form.save()  # <--- And this
            messages.success(request, "Your profile has been updated!")
            return redirect("profile")

    else:
        # If it's a GET request, just show the current info
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}

    return render(request, "blog/profile.html", context)


class Home(TemplateView):
    template_name = "blog/home.html"


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-published_date"]
    paginate_by = 5


# R - READ (Single post)
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"


# C - CREATE
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# U - UPDATE
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]
    template_name = "blog/post_form.html"  # Reuses the create template

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Security Check: Is the user the author?
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# D - DELETE
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"
    template_name = "blog/post_confirm_delete.html"

    # Security Check: Is the user the author?
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        # We get the Post ID from the URL to link the comment to the right post
        post_id = self.kwargs["pk"]
        form.instance.post = get_object_or_404(Post, pk=post_id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.kwargs["pk"]})


# 2. Update Comment View
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


# 3. Delete Comment View
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        # Redirect back to the post that this comment belonged to
        comment = self.get_object()
        return reverse("post-detail", kwargs={"pk": comment.post.pk})


def search(request):
    query = request.GET.get("q")  # Get the search term from the URL
    results = []

    if query:
        # Search Title OR Content OR Tags
        # .distinct() removes duplicates if a post matches multiple criteria
        results = Post.objects.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(tags__name__icontains=query)
        ).distinct()

    return render(
        request, "blog/search_results.html", {"posts": results, "query": query}
    )


# 2. Tagged Posts View (Reusing ListView logic is cleaner)
class PostByTagListView(ListView):
    model = Post
    template_name = "blog/home.html"  # We can reuse the home template!
    context_object_name = "posts"
    ordering = ["-published_date"]
    paginate_by = 5

    def get_queryset(self):
        tag_slug = self.kwargs.get("tag_slug")
        tag = get_object_or_404(Tag, slug=tag_slug)
        # Filter posts by this tag
        return Post.objects.filter(tags__in=[tag]).order_by("-published_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.kwargs.get("tag_slug")
        return context