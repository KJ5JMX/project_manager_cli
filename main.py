import argparse
from models import User, Project, Task
from storage import load_data, save_data
from rich.console import Console
from rich.table import Table
import json


console = Console()

def main():
    parser = argparse.ArgumentParser(description="Project Manager CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # create user
    parser_create_user = subparsers.add_parser("create-user", help="Create a new user")
    parser_create_user.add_argument("name", type=str, help="Name of the user")

    # add project
    parser_add_project = subparsers.add_parser("add-project", help="Add a project to a user")
    parser_add_project.add_argument("user_id", type=int, help="User ID")
    parser_add_project.add_argument("title", type=str, help="Project title")

    # add task
    parser_add_task = subparsers.add_parser("add-task", help="Add a task to a project")
    parser_add_task.add_argument("user_id", type=int, help="User ID")
    parser_add_task.add_argument("project_id", type=int, help="Project ID")
    parser_add_task.add_argument("description", type=str, help="Task description")

    # complete task
    parser_complete_task = subparsers.add_parser("complete-task", help="Mark a task as completed")
    parser_complete_task.add_argument("user_id", type=int, help="User ID")
    parser_complete_task.add_argument("project_id", type=int, help="Project ID")
    parser_complete_task.add_argument("task_id", type=int, help="Task ID")

     # list users
    parser_list = subparsers.add_parser("list", help="List all users, projects, and tasks")

    # delete task 
    parser_delete_task = subparsers.add_parser("delete-task", help="Delete a task from a project")
    parser_delete_task.add_argument("user_id", type=int, help="User ID")
    parser_delete_task.add_argument("project_id", type=int, help="Project ID")
    parser_delete_task.add_argument("task_id", type=int, help="Task ID to delete")

    args = parser.parse_args()
    try:
        users = [User.from_dict(u) for u in load_data()]
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        console.print(f"[red]Error loading data: {e}[/red]")
        users = []

    if args.command == "create-user":
        new_id = max([u.id for u in users], default=0) + 1
        new_user = User(id=new_id, name=args.name)
        users.append(new_user)
        console.print(f"[green]User created: {new_user}[/green]")

    elif args.command == "add-project":
        for user in users:
            if user.id == args.user_id:
                new_project_id = max([p.id for p in user.projects], default=0) + 1
                project = Project(id=new_project_id, title=args.title)
                user.add_project(project)
                print(f"Project '{args.title}' added to user ID {user.id}")
                break
        else:
            console.print(f"[red]User ID {args.user_id} not found.[/red]")

    elif args.command == "add-task":
        for user in users:
            if user.id == args.user_id:
                for project in user.projects:
                    if project.id == args.project_id:
                        new_task_id = max([t.id for t in project.tasks], default=0) + 1
                        task = Task(id=new_task_id, description=args.description)
                        project.add_task(task)
                        print(f"Task added to project ID {project.id} for user ID {user.id}")
                        break
                else:
                    print(f"Project ID {args.project_id} not found.")
                break
        else:
            print(f"User ID {args.user_id} not found.")

    elif args.command == "complete-task":
        for user in users:
            if user.id == args.user_id:
                for project in user.projects:
                    if project.id == args.project_id:
                        for task in project.tasks:
                            if task.id == args.task_id:
                                task.completed = True
                                print(f"Task ID {task.id} marked as completed.")
                                break
                        else:
                            print(f"Task ID {args.task_id} not found.")
                        break
                else:
                    print(f"Project ID {args.project_id} not found.")
                break
        else:
            print(f"User ID {args.user_id} not found.")

    elif args.command == "list":
        if not users:
            console.print("[yellow]No users found.[/yellow]")
            return

        for user in users:
            console.print(f"[bold underline]User ID {user.id}: {user.name}[/bold underline]")

            if not user.projects:
                console.print("  [yellow]No projects found.[/yellow]")
                continue

            for project in user.projects:
                console.print(f"  [bold]Project ID {project.id}: {project.title}[/bold]")

                if not project.tasks:
                    console.print("   [dim]No tasks found.[/dim]")
                    continue

                task_table = Table(show_header=True, header_style="bold magenta")
                task_table.add_column("ID", style="dim", width=6)
                task_table.add_column("Description")    
                task_table.add_column("Status", style="dim", width=12)

                
                for task in project.tasks:
                    status = "[green]Done[/green]" if task.completed else "[red]Pending[/red]"
                    task_table.add_row(str(task.id), task.description, status)

                console.print(task_table)
    
    elif args.command == "delete-task":
        for user in users:
            if user.id == args.user_id:
                for project in user.projects:
                    if project.id == args.project_id:
                        original_count = len(project.tasks)
                        project.tasks = [t for t in project.tasks if t.id != args.task_id]
                        if len(project.tasks) < original_count:
                            console.print(f"[green]Task ID {args.task_id} deleted from project ID {project.id}.[/green]")
                        else:
                            console.print(f"[red]Task ID {args.task_id} not found in project ID {project.id}.[/red]")
                        break
                else:
                    console.print(f"[red]Project ID {args.project_id} not found.[/red]")
                break
        else:
            console.print(f"[red]User ID {args.user_id} not found.[/red]")

    try:
        save_data([u.to_dict() for u in users])
    except Exception as e:
        console.print(f"[red]Error saving data: {e}[/red]")



                                        
        


if __name__ == "__main__":
    main()