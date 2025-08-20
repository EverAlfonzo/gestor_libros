from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para administrar operaciones del modelo Author a través de la API REST.

    Proporciona operaciones CRUD para autores e incluye:
    - Operaciones estándar de listado, creación, actualización y eliminación
    - Serialización completa de datos de autores
    - Acción personalizada para obtener autores ordenados por cantidad de libros

    Acciones personalizadas:
        more_books_order: Devuelve la lista de autores ordenada por cantidad de libros escritos
                         (GET /api/authors/more_books_order/)

    Campos disponibles:
        - first_name
        - last_name
        - birth_date
        - bio
        - created_at
        - updated_at
    """
    
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    @action(detail=False, methods=['get'])
    def more_books_order(self, request):
        """
        Devuelve los autores ordenados por la cantidad de libros que han escrito.
        
        Este método realiza una anotación sobre el queryset de autores,
        contando la cantidad de libros asociados a cada autor mediante la 
        relación 'books', y ordenando el resultado de forma descendente por
        dicha cantidad.
        
        Returns:
            Response: Lista serializada de autores ordenada por número de libros.
            Cada autor incluye todos sus campos junto con la cantidad de libros.
        """
        authors = Author.objects.annotate(num_books=Count('books')).order_by('-num_books')
        serializer = self.get_serializer(authors, many=True)
        return Response(serializer.data)

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet para administrar operaciones del modelo Book a través de la API REST.

    Proporciona operaciones CRUD para libros e incluye:
    - Filtrado por published_date e isbn
    - Funcionalidad de búsqueda para título, isbn y género literario
    - Queryset personalizado con prefetch_related para autores
    - Acción personalizada para obtener libros con múltiples autores

    Parámetros de filtrado:
        published_date: Filtrar libros por fecha de publicación
        isbn: Filtrar libros por ISBN
        literary_genre: Filtrar libros por género literario (no distingue mayúsculas/minúsculas)

    Campos de búsqueda:
        - título
        - isbn
        - género literario
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["published_date","isbn"]
    search_fields = ['title', 'isbn', 'literary_genre']

    def get_queryset(self):
        queryset = Book.objects.all().prefetch_related('authors')
        literary_genre = self.request.query_params.get('literary_genre')
        if literary_genre:
            queryset = queryset.filter(literary_genre__icontains=literary_genre)
        return queryset

    @action(detail=False, methods=['get'])
    def more_than_one_author(self,request):
        """
        Devuelve una lista de libros que tienen más de un autor.

        Este método realiza las siguientes operaciones:
        1. Obtiene todos los libros
        2. Anota cada libro con el número de autores que tiene
        3. Filtra para obtener solo los libros con más de un autor
        4. Serializa los resultados

        Returns:
            Response: Lista serializada de libros que tienen múltiples autores,
                     incluyendo todos los campos del modelo Book.
        """
        qs = Book.objects.all()
        qs = qs.annotate(num_authors=Count("authors")).filter(num_authors__gt=1)
        serializer = self.get_serializer(qs,many=True)
        return Response(serializer.data)
