from Account import Account
from TwoFactorAccount import TwoFactorAccount


class AccountList:
    __name = ""
    __account_list = []

    def __init__(self, name, *args):
        self.__name = name
        self.__account_list = []
        for account in args:
            if not isinstance(account, Account):
                raise ValueError(account, "is not an existing account.")
            self.__account_list = list(args)

    def __iter__(self):
        return iter(self.__account_list)

    def __str__(self):
        result = self.__name + " Accounts:\n"
        result += "Method   Website         LoginURL            Username        Password             Last PW Change    " \
                  "2F Type      Question    Q Answer    PIN\n"
        result += "-------   -------         -------             ----------      ----------           --------------    " \
                  "-------      --------    --------    ----\n"
        for account in self.__account_list:
            question = account.question if isinstance(account,
                                                      TwoFactorAccount) and account.question is not None else 'NA'
            result += F" {account.get_sec_status():7}"
            result += F" {account.get_website_name():15}"
            result += F" {account.get_loginURL():19}"
            result += F" {account.get_username():15}"
            result += F" {account.get_password():20}"
            result += F" {account.get_date_password_change():17}"
            result += F" {account.get_two_factor_type():12}"
            result += F" {question:12}"
            if account.get_answer() is not None:
                result += F" {account.get_answer():12}"
            else:
                result += " NA" + " " * 10
            # result += F" {account.get_answer():12}"
            result += F" {account.get_authentication():10}\n"
        return result

    def get_name(self):
        return self.__name

    def get_key(self):
        return self.__name.lower()

    def find(self, key):
        for account in self.__account_list:
            if key.lower() == account.get_key():
                return account
        return None

    def add(self, account):
        if account not in self.__account_list:
            self.__account_list.append(account)

    def remove(self, account):
        if account in self.__account_list:
            del(self.__account_list[self.__account_list.index(account)])
        else:
            print(account.get_key(), "does not exist as an Account + Username in the", self.__name, "List")

    def __add__(self, obj2):
        j = AccountList(self.__name + "/" + obj2.get_name())
        for account in self:
            j.add(account)
        for account in obj2:
            j.add(account)
        return j

    @staticmethod
    def build_account_list(dict):
        from Account import Account

        map = Account.get_account_map(dict)
        accounts = [map[key] for key in dict["accounts"]]
        return AccountList(dict["name"], *accounts)

    @staticmethod
    def read_data():
        from Database import Database
        return Database.read_data()

    def to_dict(self):
        return {
            "_id": self.get_key(),
            "name": self.get_name(),
            "accounts": [account.get_key() for account in self]
        }

    def save(self):
        from Database import Database

        dict = self.to_dict()
        Database.save_account_list(dict)

    def delete(self):
        from Database import Database

        Database.delete_account_list(self.get_key())