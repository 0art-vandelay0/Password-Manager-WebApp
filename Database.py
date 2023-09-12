import pymongo
from Account import  Account
from AccountList import AccountList
from dotenv import load_dotenv
import os


load_dotenv()
class Database:
    client = None

    @classmethod
    def connect(cls):
        mongodb_url = os.environ.get('MONGODB_URL')
        if cls.client is not None:
            return
        cls.client = pymongo.MongoClient(mongodb_url)
        # enter your cluster client name below in place of Cluster0
        cls.database = cls.client.Cluster0
        cls.accounts = cls.database.Accounts
        cls.account_lists = cls.database.AccountLists
        # print(cls.accounts)
        # print(cls.account_lists)

    @staticmethod
    def read_account_lists():
        from TwoFactorAccount import TwoFactorAccount
        youtube = Account("YouTube", "youtube.com/login", "herb_erlinger", "12345678", "03/22/2009")
        netflix = Account("Netflix", "netflix.com/login", "george_glass", ";thisISapasswd?", "04/22/2007")
        paypal = TwoFactorAccount("PayPal", "paypal.com/login", "dr_bitchcraft", "34567891", "05/22/2006", "Question",
                                  "What is you mother's maiden name?", "Smith", "NA")
        d2l = TwoFactorAccount("D2L", "d2l.edu/login", "user123", "myPw1989!!", "06/22/2005", "PIN", au="3344")
        pycharm = TwoFactorAccount("Pycharm", "pycharm.com/login", "456user", "56789123", "07/22/2004", "PIN",
                                   au="1122")
        gsuite = TwoFactorAccount("Google Suite", "google.com/login", "1_user_2345", "thisIsaPW!", "08/22/2003",
                                  "Question", "Where were you born?", "Oregon")
        airtable = Account("Airtable", "airtable.com/login", "U5ser_000", "123!!__pwPW", "09/22/2002")
        notion = TwoFactorAccount("Notion", "notion.com/login", "ab_user_12", "89123456", "010/22/2001", "PIN", "NA",
                                  "6660", "NA")

        media = AccountList("Media", youtube, netflix, paypal, testing)
        school = AccountList("School", d2l, pycharm, gsuite)
        work = AccountList("Work", airtable, notion)

        account_lists = [media, school, work]

        all_accounts = AccountList("All", youtube, netflix, paypal, d2l, pycharm, gsuite, airtable, notion)
        return all_accounts, account_lists

    @classmethod
    def recreate_database(cls):
        all_accounts, all_account_lists = cls.read_account_lists()
        all_account_lists.append(all_accounts)
        account_dicts = [account.to_dict() for account in all_accounts]
        account_list_dicts = [account_list.to_dict() for account_list in all_account_lists]

        cls.connect()
        cls.accounts.drop()
        cls.account_lists.drop()
        cls.accounts = cls.database.Accounts
        cls.account_lists = cls.database.AccountLists
        cls.accounts.insert_many(account_dicts)
        cls.account_lists.insert_many(account_list_dicts)

    @classmethod
    def read_data(cls):
        cls.connect()
        account_dicts = cls.accounts.find()
        account_objects = [Account.build_account(account_dict) for account_dict in account_dicts]
        map = {}
        for account in account_objects:
            map[account.get_key()] = account
        Account.set_account_map(map)
        account_list_dicts = cls.account_lists.find()
        account_list_objects = [AccountList.build_account_list(account_list_dict)
                                for account_list_dict in account_list_dicts]
        return account_list_objects

    @classmethod
    def dump_database(cls):
        account_list_objects = cls.read_data()
        for account_list_object in account_list_objects:
            print(account_list_object)

    @classmethod
    def save_account_list(cls, account_list_dict):
        cls.account_lists.update_one({"_id": account_list_dict["_id"]}, {"$set": account_list_dict}, upsert=True)

    @classmethod
    def save_account(cls, account_dict):
        cls.accounts.update_one({"_id": account_dict["_id"]}, {"$set": account_dict}, upsert=True)

    @classmethod
    def delete_account_list(cls, key):
        cls.account_lists.delete_one({"_id": key})

    def find(self, website_name, username):
        key = (website_name + " " + username).lower()
        for account in self.__account_list:
            if key == account.get_key():
                return account
        return None



if __name__ == "__main__":
    all_accounts, all_account_lists = AccountList.read_account_lists()
    account_dicts = [account.to_dict() for account in all_accounts]
    account_list_dicts = [account_list.to_dict() for account_list in all_account_lists]
    print("Accounts: ")
    for account in account_dicts:
        print(account)
    print("\nAccount Lists: ")
    for account_list_dict in account_list_dicts:
        print(account_list_dict)
    Database.recreate_database(account_dicts, account_list_dicts)
    Database.dump_database()
