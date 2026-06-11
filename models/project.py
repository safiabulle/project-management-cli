class Project:
    id_counter = 1

    def __init__(self, title, description, due_date, owner_id):
        self.id = Project.id_counter
        Project.id_counter += 1
        self.title = title
        self.description = description
        self.due_date = due_date
        self.owner_id = owner_id  # Link to User ID
        self.task_ids = []

    def __str__(self):
        return f"Project: {self.title} (Due: {self.due_date})"