class MLModel:
    def __init__(self):
        print("[MLModel] Model initialized")

    def predict(self, text: str):
        """
        Простейшее предсказание-заглушка.
        """
        return {
            "length": len(text),
            "words": len(text.split()),
            "label": "positive" if len(text) % 2 == 0 else "negative"
        }


