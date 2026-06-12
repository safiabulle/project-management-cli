from models.task import Task

def test_complete_task():
    task = Task(
        "Testing",
        1
    )

    task.complete()

    assert task.status == "Completed"