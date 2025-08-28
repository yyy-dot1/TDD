import unittest
from money import Money

class MoneyTest(unittest.TestCase):

    # ドルを掛け算するテスト
    def testMultiplication(self):
        five = Money.dollar(5)
        #5ドルに3を掛けた結果が15ドルと等しいかテスト
        self.assertEqual(Money.dollar(10), five.times(2))
        self.assertEqual(Money.dollar(15), five.times(3))

    # 通貨が同じか、違うかを比較するテスト
    def testEquality(self):
        # 5ドルと6ドルは等しくない
        self.assertEqual(Money.dollar(5), Money.dollar(5))
        # 5フランと6フランは等しくない
        self.assertNotEqual(Money.dollar(5), Money.dollar(6))
        # 5フランと5ドルは等しくない
        self.assertEqual(Money.dollar(5), Money.franc(5))

        self.assertNotEqual(Money.franc(5), Money.franc(6))

        self.assertNotEqual(Money.franc(5), Money.dollar(5))

    # フランを掛け算するテスト  
    def testFrancMultiplication(self):
        five = Money.franc(5)
        self.assertEqual(Money.franc(10), five.times(2))
        # フランに3を掛けた結果が15フランと等しいか（このテストは成功する）
        self.assertEqual(Money.franc(15), five.times(3))

    def testCurrency(self):
        self.assertEquals("USD",Money.dollar(1).currency())
        self.assertEquals("CHF",Money.franc(1).currency())

if __name__ == '__main__':
    unittest.main()