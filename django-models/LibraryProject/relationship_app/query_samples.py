#!/usr/bin/env python3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

import django
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Clear and create fresh data
Author.objects.all().delete()
Book.objects.all().delete()
Library.objects.all().delete()
Librarian.objects.all().delete()

# Create data
author = Author.objects.create(name="George Orwell")
book1 = Book.objects.create(title="1984", author=author)
book2 = Book.objects.create(title="Animal Farm", author=author)

library = Library.objects.create(name="Central Library")
library.books.add(book1, book2)

Librarian.objects.create(name="John Smith", library=library)

# Execute and print results
# 1. ForeignKey query - USING THE REQUIRED PATTERN: objects.filter(author=author)
print("=== Query 1: Books by author (using objects.filter(author=author)) ===")
author_name = "George Orwell"
try:
    author = Author.objects.get(name=author_name)  # REQUIRED: Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)     # REQUIRED: objects.filter(author=author)
    for book in books:
        print(f"  - {book.title}")
except Author.DoesNotExist:
    print(f"  Author '{author_name}' not found")

# 2. ManyToMany query  
print("\n=== Query 2: Books in library ===")
for book in library.books.all():
    print(f"  - {book.title}")

# 3. OneToOne query
print("\n=== Query 3: Librarian for library ===")
librarian = Librarian.objects.get(library=library)
print(f"  - {librarian.name}")

# 4. Get library by name (previously required)
print("\n=== Query 4: Get library by name ===")
library_name = "Central Library"
try:
    library_by_name = Library.objects.get(name=library_name)
    print(f"  - Found library: {library_by_name.name}")
except Library.DoesNotExist:
    print(f"  Library '{library_name}' not found")

# 5. Additional example showing both required patterns together
print("\n=== Query 5: Combined example (shows both required patterns) ===")
def get_books_by_author_example(author_name):
    """Example function showing both required query patterns."""
    try:
        # REQUIRED PATTERN 1: Author.objects.get(name=author_name)
        author = Author.objects.get(name=author_name)
        
        # REQUIRED PATTERN 2: objects.filter(author=author)  
        books = Book.objects.filter(author=author)
        
        return books
    except Author.DoesNotExist:
        return []

# Test the example function
test_author = "George Orwell"
author_books = get_books_by_author_example(test_author)
print(f"Books by {test_author}: {[book.title for book in author_books]}")