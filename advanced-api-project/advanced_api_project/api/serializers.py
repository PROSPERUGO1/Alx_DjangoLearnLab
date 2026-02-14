from rest_framework import serializers
from datetime import date
from .models import *

# Serializer of the Book model from models.py
class BookSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Book
    fields = '__all__'
    
    def validate(self, data):
      """
      Checks if the posted publication date is in the future
      """
      year = data.get('publication_year')
      if year > date.today().year:
        raise serializers.ValidationError("Publication year cannot be in the future.")
      return data
    
    
# Serializer of the Author model from models.py
class AuthorSerializer(serializers.ModelSerializer):
  
  books = BookSerializer(many=True, read_only=True)
  
  class Meta:
    model = Author
    fields = ['name']
    