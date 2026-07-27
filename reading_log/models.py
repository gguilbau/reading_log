from django.db import models
from django.conf import settings

# Stores one instance of a read book
class BookRead(models.Model):

    # Attach to user and allow reverse access with related name
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # Delete all books read if user is deleted
        related_name="books_read"
    )

    # Other data user will input..
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    length = models.IntegerField()

    # Use time of submission for simplicity..
    read_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author}"