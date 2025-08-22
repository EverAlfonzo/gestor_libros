from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from django.db.models import Count, Avg, Max, Min, Sum, Q
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
    permission_classes = [IsAuthenticated]

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

    @action(detail=False, methods=['get'])
    def books_statistics(self, request):
        """
        Devuelve estadísticas de los libros por autor.

        Calcula:
        - Número total de libros
        - Precio promedio de los libros
        - Libro más caro
        - Libro más barato 
        - Total de páginas escritas

        Returns:
            Response: Diccionario con las estadísticas calculadas
        """
        authors = Author.objects.annotate(
            total_books=Count('books'),
            avg_price=Avg('books__price'),
            max_price=Max('books__price'),
            min_price=Min('books__price'),
            total_pages=Sum('books__pages')
        ).values('id', 'first_name', 'last_name', 'total_books', 'avg_price', 'max_price', 'min_price', 'total_pages').order_by('last_name', 'first_name')

        result = []
        for author in authors:
            author_dict = {
                'id': author['id'],
                'first_name': author['first_name'],
                'last_name': author['last_name'],
                'total_books': author['total_books'],
                'avg_price': round(float(author['avg_price'] or 0), 2),
                'max_price': float(author['max_price'] or 0),
                'min_price': float(author['min_price'] or 0),
                'total_pages': author['total_pages'] or 0
            }
            result.append(author_dict)

        return Response(result)


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
    filterset_fields = ["published_date", "isbn"]
    search_fields = ['title', 'isbn', 'literary_genre']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Book.objects.all().prefetch_related('authors')
        literary_genre = self.request.GET.get('literary_genre')
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

    @action(detail=False, methods=['get'])
    def price_range(self, request):
        """
        Filtra libros por rango de precios.

        Query params:
        - min_price: precio mínimo
        - max_price: precio máximo

        Returns:
            Response: Lista de libros dentro del rango de precios especificado
        """
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')

        queryset = Book.objects.all()
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def advance_search(self, request):
        """
        Realiza una búsqueda compleja combinando múltiples criterios.

        Query params:
        - genre: género literario
        - min_pages: número mínimo de páginas
        - language: idioma del libro

        Returns:
            Response: Lista de libros que cumplen todos los criterios
        """
        genre = request.query_params.get('genre')
        min_pages = request.query_params.get('min_pages')
        language = request.query_params.get('language')

        query = Q()
        if genre:
            query &= Q(literary_genre__icontains=genre)
        if min_pages:
            query &= Q(pages__gte=min_pages)
        if language:
            query &= Q(language__iexact=language)

        queryset = Book.objects.filter(query)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
