import pytest
from main import BooksCollector
class TestBooksCollector:
    def test_add_new_book_add_one_book(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение')
        assert 'Гордость и предубеждение' in collector.get_books_genre()

    @pytest.mark.parametrize(
        'name, expected_result',
        [
            ('A', True),                                       
            ('1234567890123456789012345678901234567890', True), 
            ('', False),                                      
            ('12345678901234567890123456789012345678901', False)
        ]
    )
    def test_add_new_book_boundary_lengths(self, name, expected_result):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert (name in collector.get_books_genre()) == expected_result

    def test_add_new_book_duplicate_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('Дракула')
        collector.add_new_book('Дракула')
        assert len(collector.get_books_genre()) == 1

    def test_add_new_book_has_no_genre_by_default(self):
        collector = BooksCollector()
        collector.add_new_book('Оно')
        assert collector.get_book_genre('Оно') == ''

    def test_set_book_genre_valid_genre_success(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Фантастика')
        assert collector.get_book_genre('Дюна') == 'Фантастика'

    def test_set_book_genre_invalid_genre_not_set(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Роман')
        assert collector.get_book_genre('Дюна') == ''

    def test_get_books_with_specific_genre_returns_correct_list(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.add_new_book('Оно')
        collector.set_book_genre('Дюна', 'Фантастика')
        collector.set_book_genre('Оно', 'Ужасы')
        
        books_scifi = collector.get_books_with_specific_genre('Фантастика')
        assert 'Дюна' in books_scifi and 'Оно' not in books_scifi

    @pytest.mark.parametrize('genre', ['Ужасы', 'Детективы'])
    def test_get_books_for_children_excludes_age_rating_genres(self, genre):
        collector = BooksCollector()
        book_name = f'Тестовая книга {genre}'
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert book_name not in collector.get_books_for_children()

    @pytest.mark.parametrize('genre', ['Фантастика', 'Мультфильмы', 'Комедии'])
    def test_get_books_for_children_includes_safe_genres(self, genre):
        collector = BooksCollector()
        book_name = f'Детская книга {genre}'
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert book_name in collector.get_books_for_children()

    def test_favorites_lifecycle_add_duplicate_and_delete(self):
        collector = BooksCollector()
        collector.add_new_book('Шерлок Холмс')
        
        collector.add_book_in_favorites('Шерлок Холмс')
        assert 'Шерлок Холмс' in collector.get_list_of_favorites_books()
        
        collector.add_book_in_favorites('Шерлок Холмс')
        assert collector.get_list_of_favorites_books().count('Шерлок Холмс') == 1
        
        collector.delete_book_from_favorites('Шерлок Холмс')
        assert 'Шерлок Холмс' not in collector.get_list_of_favorites_books()