import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):

    def test_init(self):
        account = Account(1000.0)
        self.assertEqual(account.balance, 1000.0)
        self.assertEqual(account.holdings, {})
        self.assertEqual(account.transactions, [])
        self.assertEqual(account.initial_deposit, 1000.0)

    def test_deposit(self):
        account = Account(1000.0)
        account.deposit(500.0)
        self.assertEqual(account.balance, 1500.0)
        self.assertEqual(account.transactions[-1], {"type": "deposit", "amount": 500.0})

    def test_withdraw(self):
        account = Account(1000.0)
        self.assertTrue(account.withdraw(500.0))
        self.assertEqual(account.balance, 500.0)
        self.assertEqual(account.transactions[-1], {"type": "withdrawal", "amount": 500.0})
        self.assertFalse(account.withdraw(1000.0))

    def test_buy_shares(self):
        account = Account(1000.0)
        self.assertTrue(account.buy_shares("AAPL", 5))
        self.assertEqual(account.balance, 1000.0 - get_share_price("AAPL") * 5)
        self.assertEqual(account.holdings["AAPL"], 5)
        self.assertEqual(account.transactions[-1], {"type": "buy", "symbol": "AAPL", "quantity": 5, "price": get_share_price("AAPL")})

    def test_sell_shares(self):
        account = Account(1000.0)
        account.buy_shares("AAPL", 5)
        self.assertTrue(account.sell_shares("AAPL", 3))
        self.assertEqual(account.balance, 1000.0 - get_share_price("AAPL") * 5 + get_share_price("AAPL") * 3)
        self.assertEqual(account.holdings["AAPL"], 2)
        self.assertEqual(account.transactions[-1], {"type": "sell", "symbol": "AAPL", "quantity": 3, "price": get_share_price("AAPL")})

    def test_get_holdings(self):
        account = Account(1000.0)
        account.buy_shares("AAPL", 5)
        self.assertEqual(account.get_holdings(), {"AAPL": 5})

    def test_get_balance(self):
        account = Account(1000.0)
        account.deposit(500.0)
        account.withdraw(200.0)
        self.assertEqual(account.get_balance(), 1300.0)

    def test_get_profit_loss(self):
        account = Account(1000.0)
        account.deposit(500.0)
        account.withdraw(200.0)
        self.assertEqual(account.get_profit_loss(), 300.0)

    def test_get_transactions(self):
        account = Account(1000.0)
        account.deposit(500.0)
        account.withdraw(200.0)
        self.assertEqual(len(account.get_transactions()), 2)

if __name__ == '__main__':
    unittest.main()