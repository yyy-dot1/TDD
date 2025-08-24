class Dollar: 
    amount = 0 # これはクラス変数    
    def __init__(self, amount):
        self.amount = amount # これはインスタンス変数
    
    def times(self, multiplier): 
        return Dollar(self.amount * multiplier)
    
    def __eq__(self,other):
        #otherがDollarクラスの変数
        if isinstance(other, Dollar):
            return self.amount == other.amount
        return False