from input_validation import select_item, input_string, valid_date, valid_password
from Account import Account
from TwoFactorAccount import TwoFactorAccount
from AccountList import AccountList


class PasswordManager:
    def __init__(self):
        self.account_lists = AccountList.read_data()
        for account_list in self.account_lists:
            if account_list.get_name() == "All":
                self.all_accounts = account_list

    @staticmethod
    def print_menu():
        print("Welcome to Password Manager\n")
        print("Select an option: ")
        print("     s: Show account list Categories")
        print("     a: Add a new account list")
        print("     d: Delete an account list")
        print("     l: Select and Display accounts within a Category")
        print("     n: Add a new account to an existing list")
        print("     r: Remove account from current Account list")
        print("     j: Join two different Account Lists")
        print("     u: Update the password for an Account")
        print("     x: Exit")
        print("     m: Show Menu Options again")
        print()

    @staticmethod
    def get_choice():
        return select_item(prompt="\nWhat do you want to do? ",
                           choices=["s", "a", "d", "n", "l", "r", "j", "u", "x", "m"])

    def find_account_list(self, name):
        for account_list in self.account_lists:
            if account_list.get_name().lower() == name.lower():
                return account_list
        return None

    def find_account(self, key):
        return self.all_accounts.find(key)

    def show_account_lists(self):
        for account_list in self.account_lists:
            print(account_list.get_name())

    def add_account_list(self):
        name = input_string(
            "What is the Name/Category of the list? ",
            "Entry cannot be empty"
        )
        account_list = self.find_account_list(name)
        if account_list is not None:
            print("The list", "\"" + name + "\"", "already exists!")
            return
        account_list = AccountList(name)
        account_list.save()
        self.account_lists.append(account_list)

    def delete_account_list(self):
        name = input_string(
            "What list do you want to delete? ",
            "Entry cannot be empty"
        )
        account_list = self.find_account_list(name)
        if account_list is None:
            print("The list", "\"" + name + "\"", "does not exist!")
            return
        del(self.account_lists[self.account_lists.index(account_list)])
        account_list.delete()

    def list_accounts(self):
        name = input_string(
            "What is the List Category? ",
            "Entry cannot be empty"
        )
        account_list = self.find_account_list(name)
        if account_list is None:
            print("The list", "\"" + name + "\"", "does not exist!")
            return
        print(account_list)

    def new_account(self):
        website_name = input_string("What is the name of the website? ")
        # login_url = input_string("What is the URL to login to the website? ")
        username = input_string("What is your username for this website? ")
        key = website_name + " " + username
        account = self.find_account(key)
        if account is None:
            login_url = input_string("What is the URL to login to the website? ")
            password = input_string("What is your password for this website? ",
                                    "Password must have a least: 8 characters, one uppercase letter,\none lowercase "
                                    "letter and one of these special characters : !@#$%^&*? ", valid=valid_password)
            date_password_change = input_string("what is the date_password_change of the password change? "
                                                "(format: mm/dd/yyyy) ", valid=valid_date)
            sec_status = select_item(prompt="Do you have 1FA or 2FA for this account? ", choices=["1FA", "2FA"])

            if sec_status == "1FA":
                account = Account(website_name, login_url, username, password, date_password_change)
            elif sec_status == "2FA":
                two_factor_type = select_item(prompt="What type of security is this, PIN or Question? ",
                                              choices=["PIN", "Question"])
                if two_factor_type == "PIN":
                    authentication = input_string("What is the PIN? ")
                    question = "NA"
                    answer = "NA"
                    account = TwoFactorAccount(website_name, login_url, username, password, date_password_change,
                                               two_factor_type, question, answer, authentication)
                elif two_factor_type == "Question":
                    authentication = "NA"
                    question = input_string("What is the security question? ")
                    answer = input_string("What is the answer to the security question? ")
                    account = TwoFactorAccount(website_name, login_url, username, password, date_password_change,
                                               two_factor_type, question, answer, authentication)
            account.save()
        name = input_string(
            "What is the list Category/Name? ",
            "Entry cannot be empty"
        )
        account_list = self.find_account_list(name)
        if account_list is None:
            print("The list", "\"" + name + "\"", "does not exist!")
            return
        account_list.add(account)
        account_list.save()
        self.all_accounts.add(account)
        self.all_accounts.save()

    def remove_account(self):
        website_name = input_string("What is the website_name name? ", "Name cannot be empty")
        username = input_string("What is the username?", "Username cannot be empty")
        key = website_name + " " + username
        account = self.find_account(key)
        if account is None:
            print("No Account with site + username", key, "exists currently.")
            return
        name = input_string(
            "What is the list Category/Name? ? ",
            "Entry cannot be empty"
        )
        account_list = self.find_account_list(name)
        if account_list is None:
            print("The list", "\"" + name + "\"", "does not exist!")
            return
        account_list.remove(account)
        account_list.save()


    def join_account_lists(self):
        name1 = input_string(
            "What is the 1st Account List Name/Category? ",
            "Entry cannot be empty"
        )
        account_list1 = self.find_account_list(name1)
        if account_list1 is None:
            print("The list", "\"" + name1 + "\"", "does not exist!")
            return
        name2 = input_string(
            "What is the 2nd Account List Name/Category? ",
            "Entry cannot be empty"
        )
        account_list2 = self.find_account_list(name2)
        if account_list2 is None:
            print("The list", "\"" + name2 + "\"", "does not exist!")
            return
        new_list = account_list1 + account_list2
        exists = self.find_account_list(new_list.get_name())
        if exists is not None:
            print("Account List", exists.get_name(), "already exists.")
            return
        self.account_lists.append(new_list)
        new_list.save()

    def update_account(self):
        website_name = input_string("What is the Website name? ", "Name cannot be empty")
        username = input_string("What is the username? ", "Username cannot be empty")
        key = website_name + " " + username
        account = self.find_account(key)
        if account is None:
            print("Account", key, "does not exist!")
            return
        new_password = input_string("What is the new password for this account? ",
                                    "Password must have a least: 8 characters, one uppercase letter,\n"
                                    "one lowercase letter and one of these special characters : !@#$%^&*? ",
                                    valid=valid_password)


        print("Changing Password for", key, "from", account.get_password(), "to", new_password)
        account.set_password(new_password)
        account.save()

    def run(self):
        self.print_menu()
        while True:
            # self.print_menu()

            choice = self.get_choice()

            if choice == "x":
                return
            elif choice == "s":
                self.show_account_lists()
            elif choice == "a":
                self.add_account_list()
            elif choice == "d":
                self.delete_account_list()
            elif choice == "n":
                self.new_account()
            elif choice == "l":
                self.list_accounts()
            elif choice == "r":
                self.remove_account()
            elif choice == "j":
                self.join_account_lists()
            elif choice == "u":
                self.update_account()
            elif choice == "m":
                self.print_menu()
            else:
                print("Not a valid choice")


if __name__ == "__main__":
    app = PasswordManager()
    app.run()
