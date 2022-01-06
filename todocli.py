import typer
from rich.console import Console
from rich.table import Table
from database import *

console = Console()
app = typer.Typer()

@app.command()
def add(task: str, category: str):
    typer.echo(f"Adding task {task} in category {category}")
    todo = Todo(task, category)
    insert_todo(todo)
    show()

@app.command()
def delete(position: int):
    typer.echo(f"Deleting task {position}")
    delete_todo(position - 1)
    show()

@app.command()
def update(position: int, task: str, category: str):
    typer.echo(f"Updating task {position} to {task} in category {category}")
    update_todo(position - 1, task, category)
    show()

@app.command()
def complete(position: int):
    typer.echo(f"Completing task {position}")
    complete_todo(position - 1)
    show()

@app.command()
def show():
    todos = get_all_todos()
    console.print("[bold magenta]Todos[/bold magenta]!", "💻")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Todo", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    def get_category_color(category):
        COLORS = {'Learn': 'cyan', 'YouTube': 'red', 'Sports': 'pink', 'Study': 'green'}
        if category in COLORS:
            return COLORS[category]
        return 'white'

    for idx, task in enumerate(todos, start=1):
        c = get_category_color(task.category)
        is_done_str = '✅' if task.status == 1 else '❌'
        table.add_row(str(idx), task.task, f'[{c}]{task.category}[/{c}]', is_done_str)
    console.print(table)
    

if __name__ == "__main__":
    app()