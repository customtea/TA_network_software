import typing as tp
import json

from core.user_entry import UserEntry

def json_encode_userentry(o):
    if isinstance(o, UserEntry):
        return o.__dict__
    elif isinstance(o, bytes):
        return o.hex()
    raise TypeError(repr(o) + " is not JSON serializable")


class UserManager():
    __latest_id = 0
    __userlist:tp.Dict[int, UserEntry] = {}
    
    def __init__(self) -> None:
        pass

    def save_file(self) -> None:
        f = open("user_conf.json", "w")
        t = {}
        t["__latest_id"] = self.__latest_id
        json.dump(t, f, indent=4)
        f.close()
        
        f = open("users.json", "w")
        json.dump(self.__userlist, f,  default=json_encode_userentry, indent=4)
        f.close()
    
    def load_file(self) -> None:
        f = open("user_conf.json", "r")
        conf = json.load(f)
        t = conf["__latest_id"]
        self.__class__.__latest_id = int(t)
        f.close() 
        
        f = open("users.json", "r")
        usertable = json.load(f)
        for uid, usr in usertable.items():
            ue = UserEntry.load_dict(usr)
            self.__userlist[uid] = ue
        f.close()

    
    def add_user(self, name: str, note:tp.Any = None) -> bool:
        u = self.search_user4name(name)
        if u != None:
            print(f"{name} is exists")
            return False
        user = UserEntry.new(self.__latest_id, name, note)
        self.__userlist[self.__latest_id] = user
        self.__class__.__latest_id += 1
        return True
    
    def search_user4id(self, userid: int) -> tp.Union[UserEntry, None]:
        return self.__userlist.get(userid)
    
    def search_user4name(self, name: str) -> tp.Union[UserEntry, None]:
        for user in self.__userlist.values():
            if user.name() == name:
                return user
        return None

    def remove_user(self, userid: int) -> bool:
        if self.__userlist.get(userid) != None:
            del self.__userlist[userid]
            return True
        return False

    def set_user_entry(self, userid: int, ue: UserEntry):
        self.__userlist[userid] = ue
    
    def get_list(self) -> tp.List[UserEntry]:
        return list(self.__userlist.values())