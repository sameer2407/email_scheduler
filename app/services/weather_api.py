import requests


def get_todos(user_id=1):
    try:
        url = "https://jsonplaceholder.typicode.com/todos"
        params = {"userId": user_id}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        todos = response.json()
        return todos
    except Exception as e:
        print(f"Error fetching todos: {e}")
        return []


def format_todos_message(todos):
    if not todos:
        return ""
    
    completed = [t for t in todos if t.get("completed")]
    pending = [t for t in todos if not t.get("completed")]
    
    message = f"\n\nYour Todo Summary:\n"
    message += f"Total Tasks: {len(todos)}\n"
    message += f"Completed: {len(completed)}\n"
    message += f"Pending: {len(pending)}\n\n"
    
    if pending:
        message += "Pending Tasks:\n"
        for i, todo in enumerate(pending[:5], 1):
            message += f"{i}. {todo.get('title', 'No title')}\n"
        
        if len(pending) > 5:
            message += f"... and {len(pending) - 5} more\n"
    
    return message

