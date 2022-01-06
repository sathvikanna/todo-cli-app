class Todo:
    def __init__(self, task, category, status=0, position=None):
        self.task = task
        self.category = category
        self.status = status
        self.position = position

    def __str__(self):
        return f"{self.task} in {self.category}"