import typing as tp

from core.user_entry import UserEntry, UserType
from core.user_mgr import UserManager
from core.book_mgr import BookManager


from net.teasocket import TeaSession

class AdminLevelInterface(TeaSession):
    func_table = {}
    
    def __init__(self, user, soc) -> None:
        super().__init__(soc)
        self.user_e: UserEntry = user
        self.book_man = BookManager()
        self.user_man = UserManager()
    
    def shell(self) -> None:
        self.print("Administrator Mode")
        while True:
            # self.print("Command %")
            self.print("% ", end="")
            text = self.keywait()
            cmd_text = text.split(" ")
            if cmd_text[0].lower() == "":
                continue

            fn_cmd = self.func_table.get(cmd_text[0])
            if fn_cmd != None:
                fn_cmd(self, cmd_text)
            elif cmd_text[0] == "exit":
                break
            else:
                self.print(f"Library Command '{cmd_text[0]}' not found")
        self.print("Exit Administrator Mode")
    
    def ui_help(self, cmd_text) -> None:
        self.print("====ADMIN HELP====")
        for cmd in self.func_table:
            self.print(f"{cmd} ", end="")
        self.print("")
    
    def ui_addbook(self, cmd_text) -> None:
        if len(cmd_text) < 4:
            self.print("Not enough arguments")
            return
        else:
            title = cmd_text[1]
            author = cmd_text[2]
            if not cmd_text[3].isdecimal():
                self.print("ISBN is numeric only")
                return 
            isbn = int(cmd_text[3])
            if len(cmd_text) > 5:
                note = cmd_text[4:]
            else:
                note =None
            self.book_man.add_book(title, author, isbn, note)
            self.print("Add Book is Successful")
    
    def ui_booklist(self, cmd_text) -> None:
        for book in self.book_man.get_list():
            self.print(str(book))
    
    def ui_adduser(self, cmd_text) -> None:
        if len(cmd_text) < 2:
            self.print("Not enough arguments")
            return
        else:
            name = cmd_text[1]
            if len(cmd_text) > 3:
                note = cmd_text[3:]
            else:
                note = None
            self.user_man.add_user(name, note)
            self.print("Add User is Successful")
    
    def ui_search_user(self, cmd_text):
        if len(cmd_text) < 2:
            self.print("Not enough arguments")
            return
        else:
            name = cmd_text[1]
            user = self.user_man.search_user4name(name)
            if user == None:
                self.print("Not Found User")
            else:
                self.print(str(user))
    
    def ui_user_update(self, cmd_text):
        if len(cmd_text) < 3:
            self.print("Not enough arguments")
            return
        else:
            uid = cmd_text[1]
            utype = int(cmd_text[2])
            user = self.user_man.search_user4id(uid)
            if user == None:
                self.print("Not Found User")
            else:
                self.print(str(user))
                user.set_user_type = UserType(utype)
            self.print("UserType Upgrade is Successful")

    
    def ui_userlist(self, cmd_text) -> None:
        for user in self.user_man.get_list():
            self.print(str(user))
    

    func_table["help"] = ui_help
    func_table["addbook"] = ui_addbook
    func_table["booklist"] = ui_booklist
    func_table["adduser"] = ui_adduser
    func_table["userlist"] = ui_userlist
    func_table["finduser"] = ui_search_user
