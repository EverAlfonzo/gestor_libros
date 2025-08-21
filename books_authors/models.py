import uuid
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        abstract = True
        verbose_name = "Registro con marcas de tiempo"
        verbose_name_plural = "Registros con marcas de tiempo"


class Author(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID único")
    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellido")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Fecha de nacimiento")
    bio = models.TextField(blank=True, verbose_name="Biografía")

    class Meta:
        ordering = ["last_name", "first_name"]
        indexes = [models.Index(fields=["last_name", "first_name"])]
        verbose_name = "Autor"
        verbose_name_plural = "Autores"

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Book(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID único")
    title = models.CharField(max_length=200, verbose_name="Título")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    published_date = models.DateField(null=True, blank=True, verbose_name="Fecha de publicación")
    pages = models.PositiveIntegerField(default=0, verbose_name="Páginas")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Precio")
    language = models.CharField(max_length=30, default='Español', verbose_name="Idioma")
    literary_genre = models.CharField(max_length=50, verbose_name="Género literario")
    summary = models.TextField(blank=True, verbose_name="Resumen")
    authors = models.ManyToManyField(Author, related_name='books', verbose_name="Autores")

    class Meta:
        ordering = ["title"]
        indexes = [models.Index(fields=["title"])]
        verbose_name = "Libro"
        verbose_name_plural = "Libros"

    def __str__(self):
        return self.title
