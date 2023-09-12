from Account import Account


class TwoFactorAccount(Account):

    def __init__(self, wn, lu, un, pw, dpc, tft, qn=None, an=None, au=None):
        super().__init__(wn, lu, un, pw, dpc)
        self.two_factor_type = tft
        self.question = qn
        self.answer = an
        self.authentication = au

    # getters

    def get_sec_status(self):
        return "2FA"

    def get_two_factor_type(self):
        return self.two_factor_type

    def get_authentication(self):
        return self.authentication

    def get_question(self):
        return self.question

    def get_answer(self):
        return self.answer

    def to_dict(self):
        return {
            "_id": self.get_key(),
            "website": self.get_website_name(),
            "login url": self.get_loginURL(),
            "username": self.get_username(),
            "password": self.get_password(),
            "date pw changed": self.get_date_password_change(),
            "status": "2FA",
            "tft": self.get_two_factor_type(),
            "qn": self.get_question(),
            "an": self.get_answer(),
            "au": self.get_authentication()
        }

    # def get_PIN(self):
    #     return self.PIN

    # setters
    def set_two_factor_type(self, tft):
        self.two_factor_type = tft

    def set_authentication(self, au):
        self.authentication = au

    def set_question(self, qn):
        self.question = qn

    def set_answer(self, an):
        self.answer = an
    #
    # def set_PIN(self, pin):
    #     self.question = pin
