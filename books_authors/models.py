from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Author(TimeStampedModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        indexes = [models.Index(fields=["last_name", "first_name"])]

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Book(TimeStampedModel):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField(null=True, blank=True)
    pages = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    language = models.CharField(max_length=30, default='Español')
    literary_genre = models.CharField(max_length=50)
    summary = models.TextField(blank=True)
    authors = models.ManyToManyField(Author, related_name='books')

    class Meta:
        ordering = ["title"]
        indexes = [models.Index(fields=["title"])]

    def __str__(self):
        return self.title
