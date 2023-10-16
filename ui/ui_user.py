import typing as tp

from core.user_entry import UserEntry, UserType
from core.book_mgr import BookManager

from ui.ui_admin import AdminLevelInterface

from net.teaserver import TeaSession

class UserLevelInterface(TeaSession):
    func_table = {}
    
    def __init__(self, user, soc) -> None:
        super().__init__(soc)
        self.user_e: UserEntry = user
        self.book_man = BookManager()
    
    def shell(self) -> None:
        while True:
            # self.print("Command ?")
            text = self.keywait("> ")
            cmd_text = text.split(" ")
            if cmd_text[0].lower() == "":
                continue
            fn_cmd = self.func_table.get(cmd_text[0])
            if fn_cmd != None:
                fn_cmd(self, cmd_text)
            elif cmd_text[0] == "exit":
                break
            elif cmd_text[0] == "admin":
                if self.user_e.user_type() == UserType.ADMIN:
                    admin_ui = AdminLevelInterface(self.user_e, self.soc)
                    admin_ui.shell()
            else:
                self.print(f"Library Command '{cmd_text[0]}' not found")
    
    def ui_help(self, cmd_text) -> None:
        self.print("====HELP====")
        for cmd in self.func_table:
            self.print(f"{cmd} ", end="")
        self.print("")

    
    def ui_name(self, cmd_text) -> None:
        self.print(self.user_e.name())
    
    def ui_list(self, cmd_text) -> None:
        blist = self.user_e.get_lendinglist()
        if blist != None:
            self.print("Not Lending books")
        for bookid in blist:
            book = self.book_man.search_book4id(bookid)
            self.print(f"{book.bookid():>6} {book.title()}")
    
    def ui_searchbook(self, cmd_text):
        if len(cmd_text) < 2:
            self.print("Few Arguments")
            return
        else:
            title = cmd_text[1]
        booklist = self.book_man.search_book4title(title)
        if booklist == None:
            self.print(f"Not Find '{title}' in library")
            return 
        for book in booklist:
            self.print(f"{book.bookid():>6} {book.title()} {book.state().name}")
    

    func_table["help"] = ui_help
    func_table["name"] = ui_name
    func_table["list"] = ui_list
    func_table["search"] = ui_searchbook