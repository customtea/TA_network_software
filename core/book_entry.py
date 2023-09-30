import typing as tp
from enum import IntEnum

class BookState(IntEnum):
    STORE       = 1000
    LENDING     = 2000
    REPAIRING   = 3000
    DISCARDING  = 4000


class BookEntry():
    """BookEntry

        Attributes
        ----------
        bookid : int
            管理用書籍ID
        
        title : str
            書籍タイトル

        author : str
            著者・作者名
        
        isbn : int
            ISBN
        
        note : Any
            備考欄
        
        state : BookState
            状態 （書庫，貸出 など）
    """
    
    def __init__(self, id: int, title: str, author: str, isbn: int, note: tp.Any, state: BookState) -> None:
        self.__bookid: int = id
        self.__title: str = title
        self.__author: str = author
        self.__isbn: int = isbn
        self.__note: tp.Any = note
        self.__state: BookState = state
    
    @classmethod
    def new(cls, bid, title, author, isbn, note):
        return cls(bid, title, author, isbn, note, BookState.STORE)
    
    @classmethod
    def load(cls, bid, title, author, isbn, note, state):
        return cls(bid, title, author, isbn, note, state)

    @classmethod
    def load_dict(cls, d):
        for atr, val in d.items():
            if "__bookid" in atr:
                bid = int(val)
            elif "__title" in atr:
                title = val
            elif "__author" in atr:
                author = val
            elif "__isbn" in atr:
                isbn = int(val)
            elif "__note" in atr:
                note = val
            elif "__state" in atr:
                state = BookState(int(val))
            else:
                pass
        return cls(bid, title, author, isbn, note, state)
    
    def __str__(self) -> str:
        return f"{self.__bookid:>6} {self.__title}:{self.__author}"
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return NotImplemented
        return self.__bookid == __o.__bookid
    
    def __lt__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return NotImplemented
        return self.__bookid < __o.__bookid
    
    def bookid(self) -> int:
        return self.__bookid
    
    def title(self) -> str:
        return self.__title
    
    def author(self) -> str:
        return self.__author
    
    def ibsn(self) -> int:
        return self.__isbn
    
    def note(self) -> tp.Any:
        return self.__note
    
    def state(self) -> BookState:
        return self.__state
    
    def lending(self) -> bool:
        if self.__state != BookState.STORE:
            return False
        else:
            self.__set_state(BookState.LENDING)
            return True
    
    def back(self) -> bool:
        if self.__state != BookState.LENDING:
            return False
        else:
            self.__set_state(BookState.STORE)
            return True
    
    def __set_state(self, state: BookState):
        self.__state = state
