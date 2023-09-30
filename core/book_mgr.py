import typing as tp
import json
from core.book_entry import BookEntry

def json_encode_bookentry(o):
    if isinstance(o, BookEntry):
        return o.__dict__
    raise TypeError(repr(o) + " is not JSON serializable")

class BookManager():
    __latest_id = 0
    __booklist:tp.Dict[int, BookEntry] = {}

    def __init__(self) -> None:
        pass

    def save_file(self) -> None:
        f = open("book_conf.json", "w")
        t = {}
        t["__latest_id"] = self.__latest_id
        json.dump(t, f, indent=4)
        f.close()

        f = open("books.json", "w")
        json.dump(self.__booklist, f, default=json_encode_bookentry, indent=4)
        f.close()
        
    def load_file(self) -> None:
        f = open("book_conf.json", "r")
        conf = json.load(f)
        t = conf["__latest_id"]
        self.__class__.__latest_id = int(t)
        f.close()
        
        f = open("books.json", "r")
        booktable = json.load(f)
        for bid, bok in booktable.items():
            be = BookEntry.load_dict(bok)
            self.__booklist[bid] = be
        f.close()
    
    def add_book(self, title: str, author: str, isbn: int, note: tp.Any =None) -> bool:
        book = BookEntry.new(self.__latest_id, title, author, isbn, note)
        self.__booklist[self.__latest_id] = book
        self.__class__.__latest_id += 1
        return True
    
    def search_book4id(self, bookid: int) -> tp.Union[BookEntry, None]:
        return self.__booklist.get(bookid)
    
    def remove_book(self, bookid: int) -> bool:
        if self.__booklist.get(bookid) != None:
            del self.__booklist[bookid]
            return True
        return False
    
    def set_book_entry(self, bookid: int, be: BookEntry):
        self.__booklist[bookid] = be
    
    def search_book4title(self, title: str) -> tp.Union[tp.List[BookEntry], None]:
        res_list:tp.List[BookEntry] = []
        for bid, book in self.__booklist.items():
            if book.title() == title:
                res_list.append(book)
        return res_list
    
    def get_list(self) -> tp.List[BookEntry]:
        return list(self.__booklist.values())
    


