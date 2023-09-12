class Account:
    def __init__(self, wn, lu, un, pw, dpc):
        self.website_name = wn
        self.login_url = lu
        self.username = un
        self.password = pw
        self.date_password_change = dpc

    def __str__(self):
        return F"<{self.get_sec_status()} Account object wn={self.website_name}, lu={self.login_url}, un={self.username}, " \
               F"pw={self.password}, lcp={self.date_password_change}>"

    def __repr__(self):
        return F"<{self.get_sec_status()} Account {self.website_name} {self.login_url}>"

    def __int__(self):
        return len(self.website_name) + len(self.login_url)

    @classmethod
    def set_account_map(cls, map):
        cls.map = map

    # getters

    @classmethod
    def get_account_map(cls, map):
        return cls.map

    def get_website_name(self):
        return self.website_name

    def get_loginURL(self):
        return self.login_url

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_key(self):
        return(self.website_name + " " + self.username).lower()

    def get_name(self):
        return self.website_name + " " + self.username

    def get_date_password_change(self):
        return self.date_password_change

    def get_two_factor_type(self):
        return "NA"

    def get_authentication(self):
        return "NA"

    def get_question(self):
        return "NA"

    def get_answer(self):
        return "NA"

    def get_sec_status(self):
        return "1FA"

    def to_dict(self):
        return {
            "_id": self.get_key(),
            "website": self.get_website_name(),
            "login url": self.get_loginURL(),
            "username": self.get_username(),
            "password": self.get_password(),
            "date pw changed": self.get_date_password_change(),
            "status": "1FA",
        }

    # setters
    def set_website_name(self, website_name):
        self.website_name = website_name

    def set_login_url(self, login_url):
        self.login_url = login_url

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def date_password_change(self, date_password_change):
        self.date_password_change = date_password_change

    @staticmethod
    def build_account(dict):
        from TwoFactorAccount import TwoFactorAccount
        if dict["status"] == "1FA":
            return Account(dict["website"], dict["login url"], dict["username"], dict["password"],
                           dict["date pw changed"])
        elif dict["status"] == "2FA":
            qn = dict.get("qn")
            an = dict.get("an")
            au = dict.get("au")
            return TwoFactorAccount(dict["website"], dict["login url"], dict["username"], dict["password"],
                                    dict["date pw changed"], dict["tft"], qn, an, au)
        else:
            raise ValueError("Unknown account status:", dict["status"])

    @staticmethod
    def read_account_list():
        from AccountList import AccountList
        from TwoFactorAccount import TwoFactorAccount
        return AccountList(
            Account("test.com", "test.com/login", "user1", "thisispassword", "3/22/89"),
            Account("test2.com", "test2.com/login", "user2", "thisis2ndpassword", "4/10/89"),
            TwoFactorAccount("testTF.com", "test2FA.com/login", "user2FA", "thisis2FApass", "5/15/89", "PIN", au="6660")
        )

    def save(self):
        from Database import Database
        dict = self.to_dict()
        Database.save_account(dict)