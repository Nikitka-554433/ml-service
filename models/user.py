from datetime import datetime
from typing import List, Dict, Any

# Пользователь
class User:
    def __init__(self, user_id: int, username: str, email: str, balance: float = 0.0):
        self.__user_id = user_id
        self.username = username
        self.email = email
        self.__balance = balance
        self.role = "user"

    # Методы управления балансом
    def add_balance(self, amount: float):
        """Пополнение баланса"""
        if amount > 0:
            self.__balance += amount

    def deduct_credits(self, amount: float) -> bool:
        """Списание кредитов при анализе"""
        if self.__balance >= amount:
            self.__balance -= amount
            return True
        return False

    def get_balance(self) -> float:
        """Возврат текущего баланса"""
        return self.__balance

    def __str__(self):
        return f"User({self.username}, balance={self.__balance})"


# Администратор

class AdminUser(User):
    def __init__(self, user_id: int, username: str, email: str):
        super().__init__(user_id, username, email)
        self.role = "admin"

    def approve_topup(self, user: User, amount: float):
        """Админ пополняет баланс пользователя"""
        user.add_balance(amount)

    def view_all_transactions(self, transactions: List["Transaction"]):
        """Просмотр всех транзакций"""
        for t in transactions:
            print(t)