import sys
from core.book_mgr import BookManager
from core.user_mgr import UserManager

from ui.ui_user import UserLevelInterface

from net.teasocket import TeaServer, TeaSession

from logging import getLogger, StreamHandler, FileHandler, Formatter, INFO, ERROR, DEBUG
logger = getLogger(__name__)
logger.setLevel(DEBUG)

ch = StreamHandler(sys.stderr)
ch.setLevel(DEBUG) 
# ch_formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fmt = Formatter("%(asctime)s [%(levelname)s:%(name)s:%(funcName)s %(lineno)s] %(message)s", "%Y-%m-%dT%H:%M:%S")
ch.setFormatter(fmt)
logger.addHandler(ch)
# logger.addFilter(LoggerFilter())


# fh = FileHandler('log/test.log')
# fh.setLevel(ERROR)
# fh_formatter = Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s')
# logger.addHandler(fh) 


book_man = BookManager()
user_man = UserManager()

book_man.load_file()
user_man.load_file()


# user_man.add_user("test")
# user_man.add_user("admin")
# ue = user_man.search_user4name("admin")
# ue.set_user_type(3000)
# book_man.add_book("a","a",0)
# book_man.add_book("b","b",0)

class LibrarySession(TeaSession):
    def service(self):
        self.welcome()

    def welcome(self):
        # print(self.soc)
        logger.info(self.soc)
        
        self.print("__        __   _                            _     _ _")
        self.print("\ \      / /__| | ___ ___  _ __ ___   ___  | |   (_) |__  _ __ __ _ _ __ _   _")
        self.print(" \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | |   | | '_ \| '__/ _` | '__| | | |")
        self.print("  \ V  V /  __/ | (_| (_) | | | | | |  __/ | |___| | |_) | | | (_| | |  | |_| |")
        self.print("   \_/\_/ \___|_|\___\___/|_| |_| |_|\___| |_____|_|_.__/|_|  \__,_|_|   \__, |")
        self.print("          Created by CustomTea                                            |___/")

        for i in range(3):
            self.print("login: ",end="")
            user_name = self.keywait()
            if user_name == "exit":
                break
            org_cc, sig, res_cc = self.challnge()
            # logger.debug(f"ORGCC:{org_cc}, SIG:{sig}, RESCC:{res_cc}")
            user = user_man.search_user4name(user_name)
            if user != None and org_cc == res_cc and user.auth_pubkey(sig, org_cc.encode("utf8")):
                # print(f"{user.name()} is Authenticated")
                logger.info(f"{user.name()} is Authenticated")
                self.print(f"Welcom back {user.name()}")
                ui = UserLevelInterface(user, self.soc)
                ui.shell()
                break
            else:
                self.print("Login incorrect")
        self.close()




def main():
    TS = TeaServer(50000)
    logger.info("Socket Initialized")
    TS.session = LibrarySession
    logger.info("Server Initialized")
    try:
        logger.info("Server Start")
        TS.up()
    except KeyboardInterrupt:
        print(" Bye")
    finally:
        print("Saveing File ... ", end="")
        book_man.save_file()
        user_man.save_file()
        print("Done")



if __name__ == '__main__':
    main()