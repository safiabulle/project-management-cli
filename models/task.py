class Task:
    id_counter = 1

    def __init__(self, title, project_id):
        self.id = Task.id_counter
        Task.id_counter += 1
        self.title = title
        self.project_id = project_id
        self.status = "Pending"

    def mark_complete(self):
        self.status = "Completed"

    def __str__(self):
        return f"[{self.status}] {self.title}"