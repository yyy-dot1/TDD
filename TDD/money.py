from abc import ABC, abstractmethod

# 通貨を扱う「式」を表す抽象基底クラス
class Expression(ABC):

    @abstractmethod
    def times(self,multiplier):
        pass
    @abstractmethod
    def plus(self,addend:'Expression'):
        pass
    @abstractmethod
    def reduce(self, bank: 'Bank', to: str) -> 'Money':
        """指定された通貨に金額を換算する抽象メソッド。"""
        pass
    @abstractmethod
    def __add__(self, other: 'Expression') -> 'Expression':
        """'+' 演算子をオーバーロードするための抽象メソッド。"""
        pass

# 金額と通貨を扱うクラス
class Money(Expression):
    def __init__(self, amount: int, currency: str):
        self.amount = amount
        self._currency = currency

    def __eq__(self, other: object) -> bool:
        """2つのMoneyオブジェクトが等しいか比較する。"""
        if isinstance(other, Money):
            # 金額と通貨が両方等しいか比較
            return self.amount == other.amount and self.currency() == other.currency()
        return False

    def __repr__(self) -> str:
        """オブジェクトを開発者向けの文字列表現で返す。"""
        return f"Money({self.amount}, '{self.currency()}')"

    def __hash__(self) -> int:
        """辞書のキーとして使えるようハッシュ値を返す。"""
        return hash((self.amount, self.currency()))#金額,通貨

    def __add__(self, other: 'Expression') -> 'Expression':
        """'+' 演算子でSumオブジェクトを返す。"""
        return Sum(self, other)

    def times(self, multiplier: int) -> 'Money':
        """金額を指定された倍率で掛ける。"""
        return Money(self.amount * multiplier, self.currency())

    def currency(self) -> str:
        """通貨の種類を返す。"""
        return self._currency

    def reduce(self, bank: 'Bank', to: str) -> 'Money':
        """金額を指定された通貨に換算する。"""
        rate = bank.rate(self.currency(), to)
        # 金額を指定されたレートで換算し、新しいMoneyオブジェクトとして返す
        return Money(int(self.amount / rate), to)

    @classmethod
    def dollar(cls, amount: int) -> 'Money':
        """ドル（USD）のインスタンスを生成する。"""
        return cls(amount, "USD")

    @classmethod
    def franc(cls, amount: int) -> 'Money':
        """フラン（CHF）のインスタンスを生成する。"""
        return cls(amount, "CHF")
    
    def plus(self,addend:'Expression'):
        return Sum(self,addend)

# 2つの金額の和を表すクラス
class Sum(Expression):
    def __init__(self, augend: Expression, addend: Expression,multiplier):
        self.augend = augend #足される数
        self.addend = addend #足す数
        self.multiplier = multiplier

    def items(self,multiplier:int):
        return Sum(self.augend.times(self.multiplier),self.addend.times(self.multiplier))
    

    def reduce(self, bank: 'Bank', to: str) -> 'Money':
        """和を換算し、合計金額を返す。"""
        # augendとaddendをそれぞれreduceして、amountを足す
        amount = self.augend.reduce(bank, to).amount + self.addend.reduce(bank, to).amount
        return Money(amount, to)

    def __add__(self, other: 'Expression') -> 'Expression':
        """'+' 演算子で新しいSumオブジェクトを返す。"""
        return Sum(self, other)
    
    def plus(self,addend:'Expression'):
        return Sum(self,addend)
    
    def times(self):
        return Sum(self.augend(self.multiplier),self.addend(self.multiplier))

# 銀行クラス：通貨換算レートを管理する
class Bank:
    def __init__(self):
        """通貨ペアと換算レートを保存する辞書を初期化する。"""
        self.rates: dict['Pair', int] = {}
    def addRate(self, from_currency: str, to: str, rate: int) -> None:
        """換算レートを追加する。"""
        self.rates[Pair(from_currency, to)] = rate

    def rate(self, from_currency: str, to: str) -> int:
        """指定された通貨間のレートを取得する。"""
        # 同一通貨の処理
        if from_currency == to:
            return 1
        # 登録済みレートの取得
        # 「1」は、デフォルト値
        return self.rates.get(Pair(from_currency, to))

# 通貨ペアを表すクラス
class Pair:
    def __init__(self, from_currency: str, to: str):
        self.from_currency = from_currency
        self.to = to

    def __eq__(self, other: object) -> bool:
        """2つのPairオブジェクトが論理的に等しいか判定する。"""
        if isinstance(other, Pair):
            return self.from_currency == other.from_currency and self.to == other.to
        return False

    def hashCode(self) -> int:
        """辞書のキーとして使えるようハッシュ値を返す。"""
        return 0