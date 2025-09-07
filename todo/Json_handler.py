import json
import os
from datetime import datetime
from django.conf import settings

class JSONHandler:
    def __init__(self):
        self.json_file = os.path.join(settings.BASE_DIR, 'todos.json')
        self.ensure_json_file()
    
    def ensure_json_file(self):
        """Create JSON file if it doesn't exist"""
        if not os.path.exists(self.json_file):
            with open(self.json_file, 'w') as f:
                json.dump([], f)
    
    def load_todos(self):
        """Load todos from JSON file"""
        try:
            with open(self.json_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_todos(self, todos):
        """Save todos to JSON file"""
        with open(self.json_file, 'w') as f:
            json.dump(todos, f, indent=2)
    
    def add_todo(self, title, description=""):
        """Add a new todo"""
        todos = self.load_todos()
        new_id = max([todo.get('id', 0) for todo in todos], default=0) + 1
        
        new_todo = {
            'id': new_id,
            'title': title,
            'description': description,
            'completed': False,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        todos.append(new_todo)
        self.save_todos(todos)
        return new_todo
    
    def get_todo(self, todo_id):
        """Get a specific todo by ID"""
        todos = self.load_todos()
        return next((todo for todo in todos if todo['id'] == todo_id), None)
    
    def update_todo(self, todo_id, title=None, description=None, completed=None):
        """Update a todo"""
        todos = self.load_todos()
        for todo in todos:
            if todo['id'] == todo_id:
                if title is not None:
                    todo['title'] = title
                if description is not None:
                    todo['description'] = description
                if completed is not None:
                    todo['completed'] = completed
                todo['updated_at'] = datetime.now().isoformat()
                self.save_todos(todos)
                return todo
        return None
    
    def delete_todo(self, todo_id):
        """Delete a todo"""
        todos = self.load_todos()
        todos = [todo for todo in todos if todo['id'] != todo_id]
        self.save_todos(todos)
        return True