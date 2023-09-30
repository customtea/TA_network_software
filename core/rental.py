import typing as tp

from core.user_mgr import UserEntry
from core.book_mgr import BookEntry, BookManager


class RentalManager():
    def __init__(self, user) -> None:
        self.user_e: UserEntry = user
    
    def lending(self, book: BookEntry):
        book.lending()
        self.user_e.add_lendinglist(book.bookid())
    
    def back(self, book: BookEntry):
        self.user_e.remove_lendinglist(book.bookid())
        book.back()