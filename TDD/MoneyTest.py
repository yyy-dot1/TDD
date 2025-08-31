import unittest
from money import Bank, Expression, Money, Sum

class MoneyTest(unittest.TestCase):

    # フランを掛け算するテスト  
    def testMultiplication(self):
        five = Money.franc(5)
        self.assertEqual(Money.franc(10), five.times(2))
        # フランに3を掛けた結果が15フランと等しいか（このテストは成功する）
        self.assertEqual(Money.franc(15), five.times(3))

    # 通貨が同じか、違うかを比較するテスト
    def testEquality(self):
        # 5ドルと6ドルは等しくない
        self.assertEqual(Money.dollar(5), Money.dollar(5))
        # 5フランと6フランは等しくない
        self.assertNotEqual(Money.dollar(5), Money.dollar(6))
        # 5フランと6ドルは等しくない
        self.assertNotEqual(Money.franc(5), Money.dollar(5))

    # 通貨の種類テスト
    def testCurrency(self):
        self.assertEqual("USD",Money.dollar(1).currency())
        self.assertEqual("CHF",Money.franc(1).currency())

    def testSimpleAddition(self):
        #5ドルをfiveに格納
        five = Money.dollar(5)
        # 5ドル+5ドル=10ドル
        #sum = Money.dollar(5).plus(five)
        sum = five + five
        #５ドルにplusメソッドで5ドル加算しsumに格納
        bank = Bank()
        #Expressionに為替レートを適用することによって得られる換算結果
        reduced = bank.reduce(sum,"USD")
        #Moneyクラスの10ドルとbankクラスのsum(five.plus(five))が同じ値かどうかチェック
        self.assertEqual(Money.dollar(10),reduced)

    def testPlusReturnsSum(self):
        five = Money.dollar(5)
        result: Expression = five + five
        #five.plus(five)とSumクラスで手動で計算された結果が同じかどうかテスト
        self.assertIsInstance(result,Sum)
        self.assertEqual(five, result.augend)
        self.assertEqual(five, result.addend)  

    # 加算された結果が同じかどうかテスト
    def testReduceSum(self):
        self.sum =  Sum(Money.dollar(3),Money.dollar(4))
        bank = Bank()
        #7ドル,USD
        result = bank.reduce(self.sum,"USD")
        #Moneyクラスのインスタンスの値とresult(7ドル,USD)が同じか確認する
        self.assertEqual(Money.dollar(7),result)

    # 金額と貨幣の種類（通貨）の両方が一致しているかどうかを検証
    def testReduceMoney(self):
        bank = Bank()
        result = bank.reduce(Money.dollar(1),"USD")
        # Moneyクラスのインスタンスとreduceの結果が一致しているかどうか
        self.assertEqual(Money.dollar(1),result)

    def testReduceMoneyDifferentCurrency(self):
        bank = Bank()
        bank.addRate("CHF","USD",2)
        result = bank.reduce(Money.franc(2),"USD")
        self.assertEqual(Money.dollar(1),result)

    def testIdentityRate(self):
        self.assertEqual(1,Bank().rate("USD","USD"))

    def testMixedAddition(self):
        self.fiveBucks = Money.dollar(5)
        self.tenFrancs = Money.franc(10)
        self.bank = Bank() 
        self.bank.addRate("CHF","USD",2)
        result = self.bank.reduce(self.fiveBucks + self.tenFrancs,"USD")
        self.assertEqual(Money.dollar(10),result)

    def testSumplusMoney(self):
        self.fiveBucks = Money.dollar(5)
        self.tenFrancs = Money.franc(10)
        self.bank = Bank()
        self.bank.addRate("CHF","USD",2)
        self.sum = Sum(self.fiveBucks,self.tenFrancs).plus(self.fiveBucks)
        result = self.bank.reduce(self.sum,"USD")
        self.assertEqual(Money.dollar(15),result)

    def testSumTimes(self):
        self.fiveBucks = Money.dollar(5)
        self.tenFrancs = Money.franc(10)
        self.bank = Bank()
        self.bank.addRate("CHF","USD",2)
        self.sum = Sum(self.fiveBucks,self.tenFrancs).times(2)
        result = self.bank.reduce(self.sum,"USD")
        self.assertEqual(Money.dollar(20),result)
    
if __name__ == '__main__':
    unittest.main()