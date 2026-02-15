from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book, Author


class BookAPITests(APITestCase):
    def setUp(self):
        # 1. Create a Test User
        self.user = User.objects.create_user(username="testuser", password="password")

        # 2. Create an Author
        self.author = Author.objects.create(name="J.K. Rowling")

        # 3. Create a Book
        self.book = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author,
        )

        # 4. Define URLs (Updated for Separate Views)
        self.list_url = reverse("book-list")
        self.detail_url = reverse("book-detail", args=[self.book.id])

        # IMPORTANT: Using the specific names for your separate views
        self.create_url = reverse("book-create")
        self.update_url = reverse("book-update", args=[self.book.id])
        self.delete_url = reverse("book-delete", args=[self.book.id])

    def test_create_book_authenticated(self):
        self.client.login(username="testuser", password="password")
        data = {
            "title": "Harry Potter and the Chamber of Secrets",
            "publication_year": 1998,
            "author": self.author.id,
        }
        # CHANGE: Use self.create_url instead of self.list_url
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(
            response.data["title"], "Harry Potter and the Chamber of Secrets"
        )

    def test_update_book_authenticated(self):
        self.client.login(username="testuser", password="password")
        data = {
            "title": "Harry Potter Updated",
            "publication_year": 1997,
            "author": self.author.id,
        }
        # CHANGE: Use self.update_url instead of self.detail_url
        response = self.client.put(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Harry Potter Updated")

    def test_delete_book_authenticated(self):
        self.client.login(username="testuser", password="password")
        # CHANGE: Use self.delete_url instead of self.detail_url
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    # --- Keep the Permission & Filter tests the same, but check URL usage ---

    def test_create_book_unauthenticated(self):
        data = {
            "title": "Unauthorized Book",
            "publication_year": 2022,
            "author": self.author.id,
        }
        # CHANGE: Use self.create_url
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_unauthenticated(self):
        # CHANGE: Use self.delete_url
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_books_by_year(self):
        Book.objects.create(title="Old Book", publication_year=1950, author=self.author)
        response = self.client.get(self.list_url, {"publication_year": 1950})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books(self):
        Book.objects.create(title="Dune", publication_year=1965, author=self.author)
        response = self.client.get(self.list_url, {"search": "Dune"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books(self):
        Book.objects.create(
            title="Future Book", publication_year=2022, author=self.author
        )
        response = self.client.get(self.list_url, {"ordering": "-publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Future Book")