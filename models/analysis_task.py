# Задача анализа текста

class AnalysisTask:
    def __init__(self, task_id: int, user: User, model: MLModel, text: str):
        self.task_id = task_id
        self.user = user
        self.model = model
        self.text = text
        self.result = None
        self.status = "created"
        self.timestamp = datetime.now()

    def execute(self):
        """Запуск анализа текста"""
        if self.user.get_balance() < self.model.cost_per_request:
            self.status = "rejected: not enough balance"
            return None

        if not self.model.validate_text(self.text):
            self.status = "rejected: invalid text"
            return None

        self.result = self.model.analyze(self.text)
        self.user.deduct_credits(self.model.cost_per_request)
        self.status = "completed"
        return self.result