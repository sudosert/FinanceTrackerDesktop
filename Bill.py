
class Bill:

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


class CreditCard:

    def __init__(self, name, balance, limit, interest):
        self.name = name
        self.balance = balance
        self.limit = limit
        self.interest = interest

    @property
    def available_credit(self):
        return self.limit - self.balance


class Loan:

    def __init__(self, name, balance, limit, payment):
        self.name = name
        self.balance = balance
        self.limit = limit
        self.payment = payment

    @property
    def remaining_balance(self):
        return self.limit - self.balance

    @property
    def remaining_payments(self):
        return int(self.remaining_balance / self.payment)


class Saving:

    def __init__(self, name, total):
        self.name = name
        self.total = total
