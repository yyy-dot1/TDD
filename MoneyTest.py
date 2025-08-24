import unittest
from dollar import Dollar

class TestMoney(unittest.TestCase):
    def test_class_and_instance_equality(self):
        # Dollarクラスのインスタンスを作成し、インスタンス変数の値を設定
        five = Dollar(5)
        
        # クラス変数の値をインスタンス変数の値と同じに設定
        Dollar.amount = 5
        
        # インスタンス変数とクラス変数が等しいかテスト
        #five.amountがインスタンス変数
        #Dollar.amountがクラス変数
        self.assertEqual(five.amount, Dollar.amount)
        
        # クラス変数の値を変更し、等しくないことをテスト
        Dollar.amount = 6
        self.assertNotEqual(five.amount, Dollar.amount)

if __name__ == '__main__':
    unittest.main()