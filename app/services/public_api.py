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


def get_posts(user_id=1):
    """Fetch posts from JSONPlaceholder API for a specific user."""
    try:
        url = "https://jsonplaceholder.typicode.com/posts"
        params = {"userId": user_id}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        posts = response.json()
        return posts
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return []


def format_posts_message(posts):
    """Format posts data into a readable message."""
    if not posts:
        return ""
    
    message = f"\n\n--- Recent Posts ---\n"
    message += f"Total Posts: {len(posts)}\n\n"
    
    # Show first 3 posts with title and body preview
    for i, post in enumerate(posts[:3], 1):
        title = post.get('title', 'No title')
        body = post.get('body', '')
        # Truncate body to first 150 characters
        body_preview = body[:150] + "..." if len(body) > 150 else body
        
        message += f"Post {i}: {title}\n"
        message += f"{body_preview}\n"
        message += "-" * 50 + "\n"
    
    if len(posts) > 3:
        message += f"... and {len(posts) - 3} more posts\n"
    
    return message

