# Транзакция

class Transaction:
    def __init__(self, transaction_id: int, user: User, amount: float, t_type: str):
        self.transaction_id = transaction_id
        self.user = user
        self.amount = amount
        self.type = t_type              # 'deposit' или 'analyze'
        self.timestamp = datetime.now()

    def __str__(self):
        return f"[{self.timestamp}] {self.user.username}: {self.type} {self.amount} credits"