from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from taggit.models import Tag
from .models import Post, Comment
from .forms import (
    RegisterForm, UserUpdateForm, PostForm, 
    CommentForm, SearchForm
)

# ========== AUTHENTICATION VIEWS ==========

def register_view(request):
    """
    User registration view
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to the blog.')
            return redirect('post-list')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = RegisterForm()
    
    return render(request, 'blog/register.html', {'form': form, 'title': 'Register'})

def login_view(request):
    """
    User login view
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            return redirect('post-list')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'blog/login.html', {'title': 'Login'})

def logout_view(request):
    """
    User logout view
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('post-list')

@login_required
def profile_view(request):
    """
    User profile view - view and edit profile
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'title': 'Profile'
    }
    return render(request, 'blog/profile.html', context)


# ========== BLOG POST CRUD VIEWS ==========

class PostListView(ListView):
    """
    Display all blog posts
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Blog Posts'
        context['search_form'] = SearchForm()
        context['all_tags'] = Tag.objects.all().order_by('name')  # Get all tags for sidebar
        return context


class PostDetailView(DetailView):
    """
    Display individual blog post
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['comment_form'] = CommentForm()
        context['all_tags'] = Tag.objects.all().order_by('name')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new blog post (authenticated users only)
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')
    
    def form_valid(self, form):
        """
        Set the author to the current logged-in user
        """
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Post'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update a blog post (only author can update)
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """
        Show success message
        """
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Post'
        return context
    
    def test_func(self):
        """
        Check if the current user is the author of the post
        """
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a blog post (only author can delete)
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    context_object_name = 'post'
    
    def delete(self, request, *args, **kwargs):
        """
        Show success message on delete
        """
        messages.success(self.request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Post'
        return context
    
    def test_func(self):
        """
        Check if the current user is the author of the post
        """
        post = self.get_object()
        return self.request.user == post.author


# ========== COMMENT VIEWS ==========

class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new comment on a post
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/post_detail.html'
    
    def form_valid(self, form):
        """
        Set the author and post for the comment
        """
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        messages.success(self.request, 'Comment added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs['post_id']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update a comment (only author can update)
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        """
        Show success message
        """
        messages.success(self.request, 'Comment updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})
    
    def test_func(self):
        """
        Check if the current user is the author of the comment
        """
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a comment (only author can delete)
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def delete(self, request, *args, **kwargs):
        """
        Show success message on delete
        """
        messages.success(self.request, 'Comment deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})
    
    def test_func(self):
        """
        Check if the current user is the author of the comment
        """
        comment = self.get_object()
        return self.request.user == comment.author


# ========== SEARCH AND TAG VIEWS ==========

class SearchResultsView(ListView):
    """
    Display search results
    """
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            # Search in title, content, and tags
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct().order_by('-published_date')
        return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['title'] = f"Search Results for '{context['query']}'"
        context['all_tags'] = Tag.objects.all().order_by('name')
        return context


class TaggedPostsView(ListView):
    """
    Display posts filtered by tag
    """
    model = Post
    template_name = 'blog/tagged_posts.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return Post.objects.filter(tags__in=[self.tag]).distinct().order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['title'] = f"Posts tagged with '{self.tag.name}'"
        context['all_tags'] = Tag.objects.all().order_by('name')
        return context