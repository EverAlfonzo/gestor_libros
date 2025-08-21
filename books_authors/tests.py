import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from books_authors.models import Author, Book
from books_authors.serializers import AuthorSerializer


# --- Configuración y Fixtures ---

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_authors_and_books(db):
    # Remove existing data
    Author.objects.all().delete()
    Book.objects.all().delete()

    author1 = Author.objects.create(first_name='Gabriel', last_name='García Márquez')
    author2 = Author.objects.create(first_name='Isabel', last_name='Allende')
    author3 = Author.objects.create(first_name='Mario', last_name='Vargas Llosa')

    book1 = Book.objects.create(title='Cien años de soledad', published_date='1967-05-30', isbn='9780307474728',
                                literary_genre='Realismo mágico')
    book2 = Book.objects.create(title='El amor en los tiempos del cólera', published_date='1985-05-01',
                                isbn='9780307474278', literary_genre='Ficción')
    book3 = Book.objects.create(title='La casa de los espíritus', published_date='1982-01-01', isbn='9780307474978',
                                literary_genre='Realismo mágico')
    book4 = Book.objects.create(title='Crónica de una muerte anunciada', published_date='1981-01-01',
                                isbn='9780307474738', literary_genre='Novela')

    book1.authors.add(author1)
    book2.authors.add(author1)
    book3.authors.add(author2)
    book4.authors.add(author1, author2)

    return {
        'author1': author1,
        'author2': author2,
        'author3': author3,
        'book1': book1,
        'book2': book2,
        'book3': book3,
        'book4': book4
    }


@pytest.fixture
def test_user(db):
    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpass123')
    return user


@pytest.fixture
def auth_client(test_user):
    client = APIClient()
    url = reverse('token_obtain_pair')
    response = client.post(url, {'username': 'testuser', 'password': 'testpass123'}, format='json')
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


# --- Tests para AuthorViewSet ---

class TestAuthorViewSet:

    def test_list_authors(self, auth_client, create_authors_and_books):
        url = reverse('author-list')
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data.get('results')) == Author.objects.count()

    def test_create_author(self, auth_client, create_authors_and_books):
        url = reverse('author-list')
        data = {
            'first_name': 'Jorge Luis',
            'last_name': 'Borges',
            'birth_date': '1899-08-24',
            'bio': 'Escritor argentino.'
        }
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Author.objects.filter(first_name='Jorge Luis').exists()

    def test_retrieve_author(self, auth_client, create_authors_and_books):
        author = create_authors_and_books['author1']
        url = reverse('author-detail', kwargs={'pk': author.pk})
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        expected_data = AuthorSerializer(author).data
        assert response.data['first_name'] == expected_data['first_name']

    def test_partial_update_author(self, auth_client, create_authors_and_books):
        author = create_authors_and_books['author1']
        url = reverse('author-detail', kwargs={'pk': author.pk})
        data = {'last_name': 'Márquez'}
        response = auth_client.patch(url, data, format='json')
        author.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert author.last_name == 'Márquez'

    def test_delete_author(self, auth_client, create_authors_and_books):
        author = create_authors_and_books['author3']
        url = reverse('author-detail', kwargs={'pk': author.pk})
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Author.objects.filter(pk=author.pk).exists()

    def test_more_books_order(self, auth_client, create_authors_and_books):
        url = reverse('author-more-books-order')
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # El autor 'Gabriel García Márquez' tiene 3 libros, 'Isabel Allende' tiene 2.
        # El test asume que la vista ha sido corregida para devolver una lista ordenada de autores.
        assert response.data[0]['first_name'] == 'Gabriel'
        assert response.data[0]['last_name'] == 'García Márquez'
        assert response.data[1]['first_name'] == 'Isabel'
        assert response.data[1]['last_name'] == 'Allende'


# --- Tests para BookViewSet ---

class TestBookViewSet:

    def test_list_books(self, auth_client, create_authors_and_books):
        url = reverse('book-list')
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == Book.objects.count()

    def test_create_book(self, auth_client, create_authors_and_books):
        url = reverse('book-list')
        author =Author.objects.filter(first_name='Gabriel', last_name='García Márquez').get()
        data = {
            'title': 'Ficciones',
            'published_date': '1944-01-01',
            'isbn': '9780307474528',
            'literary_genre': 'Cuento',
            'authors_ids': [author.id]  # Usamos el ID del autor obtenido
        }
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Book.objects.filter(title='Ficciones').exists()

    def test_more_than_one_author(self, auth_client, create_authors_and_books):
        url = reverse('book-more-than-one-author')
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['title'] == 'Crónica de una muerte anunciada'

    def test_filter_by_published_date(self, auth_client, create_authors_and_books):
        url = reverse('book-list')
        response = auth_client.get(f'{url}?published_date=1982-01-01')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == 'La casa de los espíritus'

    def test_search_by_title(self, auth_client, create_authors_and_books):
        url = reverse('book-list')
        response = auth_client.get(f'{url}?search=años')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data.get('results')) == 1
        assert response.data.get('results')[0]['title'] == 'Cien años de soledad'

    def test_search_by_literary_genre(self, auth_client, create_authors_and_books):
        url = reverse('book-list')
        response = auth_client.get(f'{url}?literary_genre=realismo')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data.get('results')) == 2

    def test_filter_and_search_combined(self, auth_client, create_authors_and_books):
        url = reverse('book-list')
        response = auth_client.get(f'{url}?published_date=1985-05-01&search=el amor')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data.get('results')) == 1
        assert response.data.get('results')[0]['title'] == 'El amor en los tiempos del cólera'
