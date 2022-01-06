import sqlite3
from models import Todo

connection = sqlite3.connect('todos.db')
cursor = connection.cursor()

def create_table():
    sql = """CREATE TABLE IF NOT EXISTS todos (
        task text,
        category text,
        status integer,
        position integer
    )"""
    cursor.execute(sql)

create_table()

def insert_todo(todo):
    sql = """SELECT COUNT(*) FROM todos"""
    cursor.execute(sql)
    count = cursor.fetchone()[0]
    todo.position = count if count else 0
    sql = """INSERT INTO todos VALUES (:task, :category, :status, :position)"""
    with connection:
        cursor.execute(sql, todo.__dict__)

def get_all_todos():
    sql = """SELECT * FROM todos"""
    cursor.execute(sql)
    result = cursor.fetchall()
    todos = []
    for row in result:
        todos.append(Todo(*row))
    return todos

def delete_todo(position):
    sql = "SELECT COUNT(*) FROM todos"
    cursor.execute(sql)
    count = cursor.fetchone()[0]

    with connection:
        if position < count:
            sql = """DELETE FROM todos WHERE position = :position"""
            cursor.execute(sql, {"position": position})
            for position in range(position+1, count):
                change_position(position, position-1)

def change_position(position, new_position):
    sql = """UPDATE todos SET position = :new_position WHERE position = :position"""
    with connection:
        cursor.execute(sql, {"position": position, "new_position": new_position})

def update_todo(position, task, category):
    sql = """UPDATE todos SET task = :task, category = :category WHERE position = :position"""
    with connection:
        cursor.execute(sql, {"position": position, "task": task, "category": category})
        
def complete_todo(position):
    sql = """UPDATE todos SET status = 1 WHERE position = :position"""
    with connection:
        cursor.execute(sql, {"position": position})