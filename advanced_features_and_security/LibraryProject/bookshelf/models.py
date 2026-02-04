from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from .managers import CustomUserManager

# Create your models here.
class Book(models.Model):
  def __str__(self):
    return f"{self.title}"
  
  title = models.CharField(max_length=200)
  author = models.CharField(max_length=100)
  publication_year = models.IntegerField()
  description = models.TextField(blank=True, default='')
  
  class Meta:
    permissions = [
      ('can_view', 'Can view the book'),
      ('can_create','Can create book'),
      ('can_edit','Can edit book'),
      ('can_delete','Can delete book'),
    ]

class CustomUser(AbstractUser):
  date_of_birth = models.DateField(null=True, blank=True)
  profile_photo = models.ImageField(null=True, blank=True, upload_to="profile_photos/")
  
  objects = CustomUserManager()
  
  def __str__(self):
     return self.username
   
class CustomUserManager(BaseUserManager):
  """
  Custom manager for CustomUser model
  """
  
  def create_user(self, username, password=None, **kwargs):
    if not username:
        raise ValueError("Username must be set")

    username = self.model.normalize_username(username)
    
    user = self.model(username=username, **kwargs)
    
    if password:
        user.set_password(password)
    
    # Only default to False if not explicitly passed
    if 'is_staff' not in kwargs:
        user.is_staff = False
    if 'is_superuser' not in kwargs:
        user.is_superuser = False

    user.save(using=self._db)
    return user
  
  def create_superuser(self, username, password=None, **kwargs):
    kwargs.setdefault("is_staff", True)
    kwargs.setdefault("is_superuser", True)
    kwargs.setdefault("is_active", True)

    if kwargs.get("is_staff") is not True:
        raise ValueError("Superuser must have is_staff=True")

    if kwargs.get("is_superuser") is not True:
        raise ValueError("Superuser must have is_superuser=True")

    return self.create_user(username=username, password=password, **kwargs)