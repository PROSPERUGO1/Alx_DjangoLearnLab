from django import forms
from .models import Book

class CreateBookForm(forms.ModelForm):
  
  class Meta:
    model = Book
    fields = '__all__'
    
  def no_empty_fields(self):
    title = self.cleaned_data.get('title')
    author = self.cleaned_data.get('author')
    pub_year = self.cleaned_data.get('publication_year')
    
    if not title or title == None:
      raise forms.ValidationError("Title cannot be empty")
    if not author or author == None:
      raise forms.ValidationError("Author cannot be empty")
    if not pub_year or pub_year == None:
      raise forms.ValidationError("Publication Year cannot be empty")
    
    
class ExampleForm(forms.Form):
  text = forms.Textarea(max_length=1000)