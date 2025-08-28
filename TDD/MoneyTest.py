import unittest
from money import Money

class MoneyTest(unittest.TestCase):

    # 通貨が同じか、違うかを比較するテスト
    def testEquality(self):
        # 5ドルと6ドルは等しくない
        self.assertEqual(Money.dollar(5), Money.dollar(5))
        # 5フランと6フランは等しくない
        self.assertNotEqual(Money.dollar(5), Money.dollar(6))
        # 5フランと6ドルは等しくない
        self.assertNotEqual(Money.franc(5), Money.dollar(5))

    # フランを掛け算するテスト  
    def testFrancMultiplication(self):
        five = Money.franc(5)
        self.assertEqual(Money.franc(10), five.times(2))
        # フランに3を掛けた結果が15フランと等しいか（このテストは成功する）
        self.assertEqual(Money.franc(15), five.times(3))

    def testCurrency(self):
        self.assertEqual("USD",Money.dollar(1).currency())
        self.assertEqual("CHF",Money.franc(1).currency())
    
    def testDifferentClassEquality(self):
        self.assertNotEqual(Money.dollar(10), Money.franc(10))

if __name__ == '__main__':
    unittest.main()