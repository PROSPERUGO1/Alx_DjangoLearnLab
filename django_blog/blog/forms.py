from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from taggit.forms import TagField, TagWidget  # Make sure TagWidget is imported
from .models import Post, Comment

class RegisterForm(UserCreationForm):
    """
    Custom registration form with email field
    """
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email


class UserUpdateForm(forms.ModelForm):
    """
    Form for users to update their profile
    """
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise ValidationError("A user with this email already exists.")
        return email


class PostForm(forms.ModelForm):
    """
    Form for creating and updating blog posts with tags
    """
    # Explicitly use TagWidget for the tags field
    tags = TagField(
        required=False,
        widget=TagWidget(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas (e.g., python, django, tutorial)'
        }),
        help_text="Separate tags with commas"
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 10
            }),
        }
        labels = {
            'title': 'Post Title',
            'content': 'Post Content',
            'tags': 'Tags',
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise ValidationError("Title must be at least 5 characters long.")
        return title
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise ValidationError("Content must be at least 10 characters long.")
        return content


class CommentForm(forms.ModelForm):
    """
    Form for creating and updating comments
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 3
            }),
        }
        labels = {
            'content': '',
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 2:
            raise ValidationError("Comment must be at least 2 characters long.")
        if len(content) > 1000:
            raise ValidationError("Comment must be less than 1000 characters.")
        return content


class SearchForm(forms.Form):
    """
    Form for searching posts
    """
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search posts by title, content, or tags...'
        })
    )
    
    def clean_query(self):
        query = self.cleaned_data.get('query', '').strip()
        return query