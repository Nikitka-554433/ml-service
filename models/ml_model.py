# ML модель

class MLModel:
    """Базовый класс для всех ML моделей"""
    def __init__(self, model_name: str, cost_per_request: float):
        self.model_name = model_name
        self.cost_per_request = cost_per_request

    def validate_text(self, text: str) -> bool:
        """Простая валидация текста"""
        return isinstance(text, str) and len(text.strip()) > 0

    def analyze(self, text: str) -> Dict[str, Any]:
        """Абстрактный метод анализа"""
        raise NotImplementedError("Метод analyze() нужно реализовать в подклассе.")

# Конкретная модель анализа текста

class TextAnalyzerModel(MLModel):
    def analyze(self, text: str) -> Dict[str, Any]:
        """Имитация анализа текста"""
        words = text.split()
        score = round(min(1.0, len(words) / 100), 2)   # чем больше слов, тем “лучше”
        sentiment = "positive" if "good" in text.lower() else "neutral"
        errors = sum(1 for w in words if w.endswith("!!!"))  # условная “ошибка”
        return {
            "sentiment": sentiment,
            "errors": errors,
            "score": score
        }