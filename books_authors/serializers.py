from rest_framework import serializers
from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Author que maneja la conversión entre instancias de Author y datos JSON.

    Campos:
        - id: Identificador único del autor
        - first_name: Nombre del autor
        - last_name: Apellido del autor
        - birth_date: Fecha de nacimiento
        - bio: Biografía del autor
        - created_at: Fecha y hora de creación del registro
        - updated_at: Fecha y hora de última actualización
    """
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'birth_date', 'bio', 'created_at', 'updated_at']


class BookSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Book que maneja la conversión entre instancias de Book y datos JSON.

    Campos:
        - id: Identificador único del libro
        - title: Título del libro
        - isbn: Número Internacional Normalizado del Libro
        - published_date: Fecha de publicación
        - literary_genre: Género literario
        - pages: Número de páginas
        - price: Precio del libro
        - language: Idioma del libro
        - summary: Resumen del libro
        - authors: Serializador anidado que muestra detalles del autor (solo lectura)
        - authors_ids: Lista de IDs de autores para crear/actualizar relaciones libro-autor (solo escritura)

    El serializador proporciona un método create personalizado para manejar la relación 
    muchos a muchos entre libros y autores.
    """
    authors = AuthorSerializer(many=True, read_only=True)
    authors_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Author.objects.all(), write_only=True, source="authors")

    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'published_date', 'literary_genre', 'pages', 'price', 'language', 'summary', 'authors',
                  'authors_ids', 'created_at', 'updated_at']

    def create(self, validated_data):
        authors = validated_data.pop('authors', [])
        book = Book.objects.create(**validated_data)
        book.authors.set(authors)
        return book