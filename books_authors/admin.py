from django.contrib import admin
from .models import Author, Book


class BookInline(admin.TabularInline):
    model = Book.authors.through
    verbose_name = "Libros"
    verbose_name_plural = "Libros"
    extra = 1

class AuthorInline(admin.TabularInline):
    model = Author.books.through
    verbose_name = "Autores"
    verbose_name_plural = "Autores"
    extra = 1



@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "birth_date")
    search_fields = ("first_name", "last_name")
    inlines = [BookInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "isbn", "published_date", "pages", "price")
    list_filter = ("language",)
    exclude = ("authors",)
    search_fields = ("title", "isbn", "authors__last_name", "authors__first_name")
    inlines = [AuthorInline]
