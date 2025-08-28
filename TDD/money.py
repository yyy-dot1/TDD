from abc import ABC, abstractmethod

#ドルとフランに共通する親クラス
class Money(ABC):
    #共通のフィールド（amount）
    def __init__(self, amount:int,currency:str):
        self.amount = amount
        self._currency = currency

    @abstractmethod
    #金額を掛ける（サブクラスで実装が必要な抽象メソッド）
    def times(self, multiplier: int):
        pass

    @abstractmethod
    def currency(self):
        return self._currency
    
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
        return Dollar(amount,"USD")
    #クラスメソッド
    #Francクラスのインスタンスを生成して返す
    @classmethod
    def franc(cls, amount: int):
        return Franc(amount,"CHF")

#実装クラス
class Dollar(Money):
    def __init__(self,amount:int,currency:str):
        super().__init__(amount,currency)
    
    def times(self, multiplier: int):
        return Money.dollar(self.amount * multiplier)
    
#実装クラス
class Franc(Money):
    def __init__(self,amount,currency):
        super().__init__(amount,currency)
    
    def times(self, multiplier: int):
        return Franc(self.amount * multiplier)