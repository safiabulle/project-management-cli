from models.project import Project

def test_create_project():
    project = Project(
        "CLI Tool",
        "Project Description",
        "2026-07-01",
        1
    )

    assert project.title == "CLI Tool"