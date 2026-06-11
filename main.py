import argparse
from utils.storage import load_data, save_data
from models.user import User
from rich.console import Console

console = Console()

def handle_add_user(args):
    """
    Business logic execution for adding a user.
    """
    data = load_data()
    
    # Check if user email already exists
    if any(u["email"].lower() == args.email.lower() for u in data["users"]):
        console.print(f"[bold red]Error:[/bold red] A user with email '{args.email}' already exists.")
        return

    try:
        # Utilize our class domain for instantiation & validation
        new_user = User(name=args.name, email=args.email)
        
        # Serialize back to structural dictionary format for storage
        user_dict = {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "projects": []
        }
        
        data["users"].append(user_dict)
        save_data(data)
        
        console.print(f"[bold green]Success![/bold green] Created user [yellow]{new_user.name}[/yellow] (ID: {new_user.id})")
        
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/bold red] {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Project Management CLI Tool - Admin Panel"
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available subcommands")

    # ---- ADD USER COMMAND ----
    parser_add_user = subparsers.add_parser("add-user", help="Register a new system user")
    parser_add_user.add_argument("--name", required=True, help="Full name of the user")
    parser_add_user.add_argument("--email", required=True, help="Unique email address for user validation")

    # Parse arguments
    args = parser.parse_args()

    # Route execution to correct handler
    if args.command == "add-user":
        handle_add_user(args)

if __name__ == "__main__":
    main()