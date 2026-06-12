import argparse

from utils.storage import load_data, save_data
from models.user import User
from models.project import Project
from models.task import Task  

from rich.console import Console
from rich.table import Table

console = Console()


def handle_add_user(args):
    """
    Add a new user.
    """
    data = load_data()

    if any(
        u["email"].lower() == args.email.lower()
        for u in data["users"]
    ):
        console.print(
            f"[bold red]Error:[/bold red] A user with email '{args.email}' already exists."
        )
        return

    try:
        new_user = User(
            name=args.name,
            email=args.email
        )

        user_dict = {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "projects": []
        }

        data["users"].append(user_dict)
        save_data(data)

        console.print(
            f"[bold green]Success![/bold green] Created user "
            f"[yellow]{new_user.name}[/yellow] (ID: {new_user.id})"
        )

    except ValueError as e:
        console.print(
            f"[bold red]Validation Error:[/bold red] {e}"
        )


def handle_list_users():
    """
    Display all users.
    """
    data = load_data()

    table = Table(title="Users")

    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Email")

    for user in data["users"]:
        table.add_row(
            str(user["id"]),
            user["name"],
            user["email"]
        )

    console.print(table)


def handle_add_project(args):
    """
    Add a project to a user.
    """
    data = load_data()

    user = next(
        (
            u for u in data["users"]
            if u["name"].lower() == args.user.lower()
        ),
        None
    )

    if not user:
        console.print(
            "[bold red]Error:[/bold red] User not found."
        )
        return

    project = Project(
        args.title,
        args.description,
        args.due_date,
        user["id"]
    )

    project_dict = {
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "due_date": project.due_date,
        "owner_id": project.owner_id,
        "tasks": []
    }

    data["projects"].append(project_dict)
    save_data(data)

    console.print(
        f"[bold green]Success![/bold green] "
        f"Project '{project.title}' created."
    )


def handle_list_projects():
    """
    Display all projects.
    """
    data = load_data()

    table = Table(title="Projects")

    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Description")
    table.add_column("Due Date")
    table.add_column("Owner ID")

    for project in data["projects"]:
        table.add_row(
            str(project["id"]),
            project["title"],
            project["description"],
            project["due_date"],
            str(project["owner_id"])
        )

    console.print(table)

def handle_add_task(args):
    """
    Add a task to a project.
    """
    data = load_data()

    project = next(
        (
            p for p in data["projects"]
            if p["title"].lower() == args.project.lower()
        ),
        None
    )

    if not project:
        console.print(
            "[bold red]Error:[/bold red] Project not found."
        )
        return

    # Generate the next task ID from stored data
    next_id = 1

    if data["tasks"]:
        next_id = max(task["id"] for task in data["tasks"]) + 1

    task = Task(
        args.title,
        project["id"]
    )

    task.id = next_id

    task_dict = {
        "id": task.id,
        "title": task.title,
        "project_id": task.project_id,
        "status": task.status
    }

    data["tasks"].append(task_dict)
    save_data(data)

    console.print(
        f"[bold green]Success![/bold green] Task '{task.title}' added."
    )




def handle_list_tasks():
    """
    Display all tasks.
    """
    data = load_data()

    table = Table(title="Tasks")

    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Project ID")
    table.add_column("Status")

    for task in data["tasks"]:
        table.add_row(
            str(task["id"]),
            task["title"],
            str(task["project_id"]),
            task["status"]
        )

    console.print(table)


def handle_complete_task(args):
    """
    Mark a task as completed.
    """
    data = load_data()

    for task in data["tasks"]:
        if task["id"] == args.task_id:
            task["status"] = "Completed"

            save_data(data)

            console.print(
                f"[bold green]Success![/bold green] Task {args.task_id} completed."
            )
            return

    console.print(
        "[bold red]Error:[/bold red] Task not found."
    )


def main():
    parser = argparse.ArgumentParser(
        description="Project Management CLI Tool"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="Available commands"
    )

    # ----------------------------
    # ADD USER
    # ----------------------------
    parser_add_user = subparsers.add_parser(
        "add-user",
        help="Register a new user"
    )

    parser_add_user.add_argument(
        "--name",
        required=True,
        help="User name"
    )

    parser_add_user.add_argument(
        "--email",
        required=True,
        help="User email"
    )

    # ----------------------------
    # LIST USERS
    # ----------------------------
    subparsers.add_parser(
        "list-users",
        help="Display all users"
    )

    # ----------------------------
    # ADD PROJECT
    # ----------------------------
    parser_add_project = subparsers.add_parser(
        "add-project",
        help="Create a project"
    )

    parser_add_project.add_argument(
        "--user",
        required=True,
        help="Owner of the project"
    )

    parser_add_project.add_argument(
        "--title",
        required=True,
        help="Project title"
    )

    parser_add_project.add_argument(
        "--description",
        default="",
        help="Project description"
    )

    parser_add_project.add_argument(
        "--due-date",
        default="Not Set",
        help="Project due date"
    )

    # ----------------------------
    # LIST PROJECTS
    # ----------------------------
    subparsers.add_parser(
        "list-projects",
        help="Display all projects"
    )

    # ----------------------------
    # ADD TASK
    # ----------------------------
    parser_add_task = subparsers.add_parser(
        "add-task",
        help="Add a task to a project"
    )

    parser_add_task.add_argument(
        "--project",
        required=True,
        help="Project title"
    )

    parser_add_task.add_argument(
        "--title",
        required=True,
        help="Task title"
    )

    # ----------------------------
    # LIST TASKS
    # ----------------------------
    subparsers.add_parser(
        "list-tasks",
        help="Display all tasks"
    )

    # ----------------------------
    # COMPLETE TASK
    # ----------------------------
    parser_complete_task = subparsers.add_parser(
        "complete-task",
        help="Mark a task as completed"
    )

    parser_complete_task.add_argument(
        "--task-id",
        type=int,
        required=True,
        help="Task ID"
    )

    args = parser.parse_args()

    # ----------------------------
    # ROUTING
    # ----------------------------
    if args.command == "add-user":
        handle_add_user(args)

    elif args.command == "list-users":
        handle_list_users()

    elif args.command == "add-project":
        handle_add_project(args)

    elif args.command == "list-projects":
        handle_list_projects()

    elif args.command == "add-task":
        handle_add_task(args)

    elif args.command == "list-tasks":
        handle_list_tasks()

    elif args.command == "complete-task":
        handle_complete_task(args)


if __name__ == "__main__":
    main()