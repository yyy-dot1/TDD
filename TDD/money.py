from abc import ABC, abstractmethod

#ドルとフランに共通する親クラス
class Money(ABC):
    #共通のフィールド（amount）
    def __init__(self, amount):
        self.amount = amount
    @abstractmethod
    #金額を掛ける（サブクラスで実装が必要な抽象メソッド）
    def times(self, multiplier: int):
        pass
    
    #共通のメソッド（金額と通貨が等しいか比較する）
    #引数の説明
    # self：Moneyクラスのインスタンス
    # other:任意のクラスのインスタンス
    # assertTrue(Money.dollar(5)←<<SELF>>.equals(Money.dollar(5)←<<OTHER>>));
    def __eq__(self,other):
        # 比較対象がMoneyクラス（またはそのサブクラス）のインスタンスかチェック
            # 金額が等しいかチェック
            # インスタンスのクラス（通貨の種類）が等しいかチェック(FrancクラスとかDollarクラスとか)
        return isinstance(other, Money) and self.amount == other.amount and self.__class__ is other.__class__
    
    #クラスメソッド
    #Dollarクラスのインスタンスを生成して返す
    @classmethod
    def dollar(cls, amount: int):
        return Dollar(amount)
    #クラスメソッド
    #Francクラスのインスタンスを生成して返す
    @classmethod
    def franc(cls, amount: int):
        return Franc(amount)

#実装クラス
class Dollar(Money):
    def times(self, multiplier: int):
        return Dollar(self.amount * multiplier)
#クラスメソッドとインスタンスメソッドを比較
    def __eq__(self, other):
        return isinstance(other, Dollar) and self.amount == other.amount
#実装クラス
class Franc(Money):
    def times(self, multiplier: int):
        return Franc(self.amount * multiplier)
#クラスメソッドとインスタンスメソッドを比較
    def __eq__(self, other):
        return isinstance(other, Franc) and self.amount == other.amount