from flask import Flask, render_template, request
from AccountList import AccountList
from input_validation import valid_password, select_item, input_string
from Account import Account
from TwoFactorAccount import TwoFactorAccount


class WebPasswordManager:
    app = Flask(__name__)

    @staticmethod
    @app.route("/")
    @app.route("/index")
    @app.route("/index.html")
    @app.route("/index.php")
    @app.route("/style.css")
    def homepage():
        menu_choices = {
            "/show_account_lists": "Show Account Category lists.",
            "/add_account_list_form": "Add a new Account List/Category.",
            "/delete_account_list_form": "Delete an existing Account List/Category.",
            "/new_account_form": "Create a new account.",
            "/add_account_to_list_form": "Move an Account to an Account List/Category.",
            "/remove_account_from_list_form": "Remove an Account from an Account List/Category.",
            "/update_account_form": "Update your password for an Account.",
            "/join_lists_form": "Join two Account Lists.",
            "/delete_account_form": "Delete an Account."
        }
        return render_template("index.html", menu_choices=menu_choices)

    @staticmethod
    @app.route("/default")
    def default():
        return render_template("default.html")

    @staticmethod
    def find_account_list(name):
        for account_list in WebPasswordManager.account_lists:
            if account_list.get_name() == name:
                # if account_list.get_name().lower() == name.lower():
                return account_list
        return None

    @staticmethod
    def find_account(key):
        return WebPasswordManager.all_accounts.find(key)

    @staticmethod
    @app.route("/show_account_lists")
    def show_account_lists():
        return render_template("account_lists.html", account_lists=WebPasswordManager.account_lists)

    @staticmethod
    @app.route("/account_list_accounts")
    def account_list_accounts():
        print(request)
        name = request.args["name"]
        account_list = WebPasswordManager.find_account_list(name)
        return render_template("account_list_accounts.html", account_list=account_list)
        return "<pre>" + str(WebPasswordManager.find_account_list(name)) + "</pre>"

    @staticmethod
    @app.route("/add_account_list_form")
    def add_account_list_form():
        return render_template("add_account_list_form.html")

    @staticmethod
    @app.route("/add_account_list")
    def add_account_list():
        name = request.args["name"]
        account_list = WebPasswordManager.find_account_list(name)
        if account_list is not None:
            return render_template("error.html", error_header="nope.", error="the list " "\"" + name + "\"" " already "
                                                                                                       "exists")
        print("Adding:", name)
        account_list = AccountList(name)
        account_list.save()
        WebPasswordManager.account_lists.append(account_list)
        return render_template("account_list_added.html", name=name)

    @staticmethod
    @app.route("/new_account_form")
    def new_account_form():
        return render_template("new_account_form.html")

    @staticmethod
    @app.route("/choose_account_status")
    def choose_account_status():
        status = request.args["status"]
        if status == "1FA":
            return render_template("new_1fa_account_form.html")
        elif status == "2FA":
            return render_template("new_2fa_account_form.html")
        else:
            return render_template("error.html", error_header="nope.", error="\"" + status + "\""
                                                                                             "is not a valid status")

    @staticmethod
    @app.route("/new_account", methods=['POST'])
    def new_account():
        if request.method == 'POST':
            website_name = request.form["website_name"]
            login_url = request.form["loginURL"]
            username = request.form["username"]
            password = request.form["password"]
            date_password_change = request.form["date_last_changed"]
            sec_status = request.form["status"]
            key = website_name + " " + username
            account = WebPasswordManager.find_account(key)
            if account is not None:
                return render_template("error.html", error_header="nope.", error="The account " + "\"" + key + "\"" +
                                                                                 " already exists")
            if not valid_password(password):
                return render_template("error.html", error_header="nope.", error="invalid password.")
            if sec_status == "1FA":
                account = Account(website_name, login_url, username, password, date_password_change)
            elif sec_status == "2FA":
                two_factor_type = request.form["two_factor_type"]
                if two_factor_type == 'question':
                    question = request.form['question']
                    answer = request.form['answer']
                    authentication = 'NA'
                else:
                    question = 'NA'
                    answer = 'NA'
                    authentication = request.form['authentication']
                if authentication is None:
                    return "NA"
                account = TwoFactorAccount(website_name, login_url, username, password, date_password_change,
                                           two_factor_type, question, answer, authentication)
            else:
                return render_template("error.html", error_header="nope.", error="Account status is 1FA or 2FA")
            account.save()
            WebPasswordManager.all_accounts.add(account)
            WebPasswordManager.all_accounts.save()
            return render_template("new_account_added.html", name=key)

    @staticmethod
    @app.route("/add_account_to_list_form")
    def add_account_to_list_form():
        return render_template(
            "/add_account_to_list_form.html",
            accounts=WebPasswordManager.all_accounts,
            account_lists=WebPasswordManager.account_lists)

    @staticmethod
    @app.route("/add_account_to_list")
    def add_account_to_list():
        account_name = request.args["account_name"]
        account_list_name = request.args["account_list_name"]
        account = WebPasswordManager.all_accounts.find(account_name)
        if account is None:
            return render_template("error.html", error_header="nope.", error="Account " + "\"" + account_name + "\"" +
                                                                             " does not exist")
        account_list = WebPasswordManager.find_account_list(account_list_name)
        if account is None:
            return render_template("error.html", error_header="nope.", error="Account List " + "\"" + account_list_name
                                                                             + "\"" + " does not exist")
        if account in account_list:
            return render_template("error.html", error_header="nope.", error="\"" + account_name
                                                                             + "\"" + " is where it needs to be in "
                                                                             + account_list_name)
        account_list.add(account)
        account_list.save()
        return render_template("account_added_to_list.html", account=account, account_list_name=account_list_name)

    @staticmethod
    @app.route("/remove_account_from_list_form")
    def remove_account_from_list_form():
        return render_template(
            "/remove_account_from_list_form.html",
            accounts=WebPasswordManager.all_accounts,
            account_lists=WebPasswordManager.account_lists)

    @staticmethod
    @app.route("/remove_account_from_list")
    def remove_account_from_list():
        account_name = request.args["account_name"]
        account_list_name = request.args["account_list_name"]
        account = WebPasswordManager.all_accounts.find(account_name)
        if account is None:
            return render_template("error.html", error_header="nope.", error="Account " + "\"" + account_name + "\"" +
                                                                             " does not exist")
        account_list = WebPasswordManager.find_account_list(account_list_name)
        if account is None:
            return render_template("error.html", error_header="nope.", error="Account List " + "\"" + account_list_name
                                                                             + "\"" + " does not exist")
        account_list.remove(account)
        account_list.save()
        return render_template("account_removed_from_list.html", account=account, account_list_name=account_list_name)

    @staticmethod
    @app.route("/delete_account_list_form")
    def delete_account_list_form():
        return render_template("delete_account_list_form.html", account_lists=WebPasswordManager.account_lists)

    @staticmethod
    @app.route("/delete_account_list")
    def delete_account_list():
        name = request.args["name"]
        account_list = WebPasswordManager.find_account_list(name)
        if account_list is None:
            return render_template("error.html", error_header="nope.", error="the list " "\"" + name + "\"" "doesn't "
                                                                                                       "exist")
        print("deleting:", name)
        del (WebPasswordManager.account_lists[WebPasswordManager.account_lists.index(account_list)])
        account_list.delete()
        return render_template("account_list_deleted.html", name=name)

    @staticmethod
    @app.route("/update_account_form")
    def update_account_form():
        return render_template(
            "/update_account_form.html", accounts=WebPasswordManager.all_accounts)

    @staticmethod
    @app.route("/update_account", methods=["POST"])
    def update_account():
        if request.method == 'POST':
            account_name = request.form["account_name"]
            account = WebPasswordManager.all_accounts.find(account_name)
            if account is None:
                return render_template("error.html", error_header="nope.",
                                       error="Account " + "\"" + account_name + "\"" + " does not exist")
            new_password = request.form["new_password"]
            account.set_password(new_password)
            account.save()
            return render_template("/account_updated.html", account=account_name)

    @staticmethod
    @app.route("/join_lists_form")
    def join_lists_form():
        return render_template(
            "/join_lists_form.html",
            account_lists=WebPasswordManager.account_lists)

    @staticmethod
    @app.route("/join_lists")
    def join_lists():
        account_list_name1 = request.args["account_list_name1"]
        account_list_name2 = request.args["account_list_name2"]

        for account_list in WebPasswordManager.account_lists:
            if account_list_name1 in account_list.get_name() and account_list_name2 in account_list.get_name():
                return render_template("error.html", error_header="nope.",
                                       error="the list combo " + "\"" + account_list_name1 + "\"" + " + " + "\""
                                             + account_list_name2 + "\"" + " already exists")

        account_list1 = WebPasswordManager.find_account_list(account_list_name1)
        account_list2 = WebPasswordManager.find_account_list(account_list_name2)

        new_list = account_list1 + account_list2
        new_list.save()
        WebPasswordManager.account_lists.append(new_list)
        return render_template("account_lists_joined.html", account_list_name1=account_list_name1,
                               account_list_name2=account_list_name2)

    @staticmethod
    @app.route("/delete_account_form")
    def delete_account_form():
        return render_template("delete_account_form.html", accounts=WebPasswordManager.all_accounts)

    @staticmethod
    @app.route("/delete_account")
    def delete_account():
        account_name = request.args["account_name"]
        account = WebPasswordManager.all_accounts.find(account_name)
        if account is None:
            return render_template("error.html", error_header="nope.",
                                   error="Account " + "\"" + account_name + "\"" + " does not exist")
        # account_list = WebPasswordManager.find_account_list(account)
        # if account_list is None:
        #     return render_template("error.html", error_header="nope.", error="There was an error deleting the account.")
        WebPasswordManager.all_accounts.remove(account)
        WebPasswordManager.all_accounts.save()
        return render_template("account_deleted.html", account=account)


    @staticmethod
    @app.route('/error')
    def error():
        return render_template('error.html')

    @staticmethod
    def run():
        WebPasswordManager.account_lists = AccountList.read_data()
        for account_list in WebPasswordManager.account_lists:
            if account_list.get_name() == "All":
                WebPasswordManager.all_accounts = account_list
        WebPasswordManager.app.run(port=8080)


if __name__ == "__main__":
    WebPasswordManager.run()
