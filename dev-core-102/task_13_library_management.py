class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True

    def display_info(self):
        availability = "Доступна" if self.is_available else "Недоступна"
        return f"\"{self.title}\" — {self.author} ({availability})"

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def list_available_books(self):
        return [book for book in self.books if book.is_available]

    def borrow_book(self, title, user):
        book = next((book for book in self.books if book.title.lower() == title.lower() and book.is_available), None)
        if book:
            book.is_available = False
            user.borrow_book(book)
            return f"Книга \"{book.title}\" успешно выдана {user.name}."
        else:
            return f"Книга \"{title}\" либо недоступна, либо не существует."

    def return_book(self, title):
        book = next((book for book in self.books if book.title.lower() == title.lower() and not book.is_available), None)
        if book:
            book.is_available = True
            return f"Книга \"{book.title}\" снова доступна."
        else:
            return f"Книга \"{title}\" не была взята или не существует."

class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.borrowed_books_list = []

    def borrowed_books(self):
        return [book.title for book in self.borrowed_books_list]

    def borrow_book(self, book):
        self.borrowed_books_list.append(book)

if __name__ == "__main__":
    library = Library()

    book1 = Book("1984", "Джордж Оруэлл", "97")
    book2 = Book("Мастер и Маргарита", "Михаил Булгаков", "98")
    book3 = Book("Қыз Жібек", "Жүсіпбек Аймауытов", "99")
    book4 = Book("Абай жолы", "Мұхтар Әуезов", "100")
    book5 = Book("Преступление и наказание", "Федор Достоевский", "101")
    
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)
    library.add_book(book4)
    library.add_book(book5)

    print("Доступные книги в библиотеке:")
    available_books = library.list_available_books()
    for i, book in enumerate(available_books, 1):
        print(f"{i}. {book.display_info()}")

    user_name = input("\nВведите имя пользователя: ")
    user = User(user_name, 1)

    book_title = input(f"{user_name}, введите название книги, которую хотите взять: ")
    print(library.borrow_book(book_title, user))

    print("\nДоступные книги в библиотеке:")
    available_books = library.list_available_books()
    for i, book in enumerate(available_books, 1):
        print(f"{i}. {book.display_info()}")

    return_title = input(f"\n{user_name} возвращает книгу \"{book_title}\": ")
    print(library.return_book(return_title))

    print("\nДоступные книги в библиотеке:")
    available_books = library.list_available_books()
    for i, book in enumerate(available_books, 1):
        print(f"{i}. {book.display_info()}")
