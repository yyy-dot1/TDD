from abc import ABC, abstractmethod

# 通貨を扱う「式」を表す抽象基底クラス
class Expression(ABC):

#具体的な金額を単純に掛け算する
    @abstractmethod
    def times(self,multiplier):
        pass

# 既存のSumオブジェクトに、さらに別のExpressionオブジェクトを足す
    @abstractmethod
    def plus(self,addend:'Expression'):
        pass
    @abstractmethod

# 式に含まれるすべての要素を換算し、その合計を算出する
    # (例)
    # 5ドルをドルに換算（そのまま5ドル）
    # 10フランをドルに換算（例えば、10フランが2ドルだった場合）
    # 換算した両方の金額を足し合わせる（5ドル + 2ドル = 7ドル）
    # 最終的な金額である7ドルのMoneyオブジェクトを返す。
    def reduce(self, bank: 'Bank', to: str) -> 'Money':
        """指定された通貨に金額を換算する抽象メソッド。"""
        pass

#「オブジェクト同士の加算」という複雑な処理を、
# Pythonの組み込み機能である+演算子に結びつける
    @abstractmethod
    def __add__(self, other: 'Expression') -> 'Expression':
        """'+' 演算子をオーバーロードするための抽象メソッド。"""
        pass

# 具体的な金額と通貨（例：5ドル、10フラン）を扱うクラス
class Money(Expression):
    def __init__(self, amount: int, currency: str):
        self.amount = amount
        self._currency = currency
        
# 2つのMoneyオブジェクトが等しいか比較する
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Money):
            # 金額と通貨が両方等しいか比較
            return self.amount == other.amount and self.currency() == other.currency()
        return False

# オブジェクトを開発者向けの文字列表現で返す
    def __repr__(self) -> str:
        return f"Money({self.amount}, '{self.currency()}')"

# 辞書のキーとして使えるようハッシュ値を返す
    def __hash__(self) -> int:
        return hash((self.amount, self.currency()))#金額,通貨

# '+' 演算子でSumオブジェクトを返す
    def __add__(self, other: 'Expression') -> 'Expression':
        return Sum(self, other)

# 金額を指定された倍率で掛ける
# 元の金額（self.amount）に倍率（multiplier）を掛け、新しい金額を算出
    def times(self, multiplier: int) -> 'Expression':
        return Money(self.amount * multiplier, self.currency())

# 通貨の種類を返す
    def currency(self) -> str:
        return self._currency

# 金額を指定された通貨に換算する
# 次の行で実際の金額（self.amount）を換算するために使用する
    def reduce(self, bank: 'Bank', to: str) -> 'Money':
        rate = bank.rate(self.currency(), to)
        # 金額を指定されたレートで換算し、新しいMoneyオブジェクトとして返す
        return Money(int(self.amount / rate), to)

# ドル（USD）のインスタンスを生成する
    @classmethod
    def dollar(cls, amount: int) -> 'Money':
        return cls(amount, "USD")
# フラン（CHF）のインスタンスを生成する
    @classmethod
    def franc(cls, amount: int) -> 'Money':
        return cls(amount, "CHF")

# 既存の計算式に新しい要素を追加する 
    def plus(self,addend:'Expression'):
        return Sum(self,addend)

# 2つの「お金の式」を一つの「計算式」としてまとめる
    # すぐに計算せずに、後からまとめて換算できるよう、式を覚えておく
class Sum(Expression):
    def __init__(self, augend: Expression, addend: Expression):
        self.augend = augend #足される数
        self.addend = addend #足す数

# 要素ごとの乗算: self.augend.times(multiplier)とself.addend.times(multiplier)を呼び出して、
# 式に含まれるそれぞれの要素（augendとaddend）に倍率を適用する
    def times(self,multiplier:int):
        # 新しいSumの生成
        return Sum(self.augend.times(multiplier),self.addend.times(multiplier))

# 和を換算し、合計金額を返す
    def reduce(self, bank: 'Bank', to: str) -> 'Money':
        # augendとaddendをそれぞれ換金して、amountを足す
        amount = self.augend.reduce(bank, to).amount + self.addend.reduce(bank, to).amount
        return Money(amount, to)

# '+' 演算子で新しいSumオブジェクトを返す
    def __add__(self, other: 'Expression') -> 'Expression':
        return Sum(self, other)
    
# Sumという未解決の計算式に、新しい要素（addend）を加えて、
# 新しいSumオブジェクトを生成して返す
    def plus(self,addend:'Expression'):
        return Sum(self,addend)
    
# 異なる通貨間の「換算レート」を管理するクラス
class Bank:
    # 通貨ペアと換算レートを保存する辞書を初期化する
    def __init__(self):
        self.rates: dict['Pair', int] = {}
# 換金実行メソッド
    def reduce(self,source:Expression,to:str):
        return source.reduce(self,to)
    
# 換算レートを登録する
    def add_rate(self, from_currency: str, to: str, rate: int) -> None:
        self.rates[Pair(from_currency, to)] = rate

# 指定された2つの通貨間の換算レートを、
# Bankに登録された情報から探し出して返す
    def rate(self, from_currency: str, to: str) -> int:
       # 通貨が同じ場合:レートは1
        if from_currency == to:
            return 1
        # 通貨が異なる場合:通貨の組み合わせを表すPairオブジェクトを作成
        pair = Pair(from_currency, to)

        # レートが存在しない場合
        if pair not in self.rates:
            #エラーメッセージ
            raise ValueError(f"Rate not found for {from_currency} to {to}")
        # レートが存在する場合
            #対応する換算レート（整数値）を取得し、返す
        return self.rates[pair]

# 「どの通貨からどの通貨へ」というペア（組み合わせ）を表現する
class Pair:
    def __init__(self, from_currency: str, to: str):
        self.from_currency = from_currency
        self.to = to

# 2つのPairオブジェクトが論理的に等しいか判定する
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Pair):
            return self.from_currency == other.from_currency and self.to == other.to
        return False
# Pairオブジェクトを一意に識別するためのハッシュ値を生成
    def __hash__(self) -> int:
        return hash((self.from_currency, self.to))