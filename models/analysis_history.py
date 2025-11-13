# История анализов

class AnalysisHistory:
    def __init__(self):
        self.records: List[AnalysisTask] = []

    def add_record(self, task: AnalysisTask):
        self.records.append(task)

    def get_history_for_user(self, user: User) -> List[AnalysisTask]:
        return [t for t in self.records if t.user == user]