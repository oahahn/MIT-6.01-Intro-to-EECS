class AccountDollars:
    """Represents a bank account in dollars"""
    def __init__(self, initialBalance):
        self.balance = initialBalance
        self.interestRate = 0.1
        #self.fee = 20
    def depositDollars(self, deposit):
        self.balance = self.balance * (1 + self.interestRate) + deposit
        return self.balance

class AccountPounds(AccountDollars):
    """
    Represents a bank account in pounds. Inherits most information from the
    parent class
    """ 
    def __init__(self, initialBalance):
        # There are 2 dollars to a pound
        AccountDollars.__init__(self, initialBalance * 2)
    def depositPounds(self, deposit):
        return self.depositDollars(deposit * 2) / 2