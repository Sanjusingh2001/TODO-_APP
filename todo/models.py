from django.db import models
import json
import os
from django.conf import settings
from datetime import datetime
from django.db import models

class TodoManager:
    def __init__(self):
        self.file_path = settings.JSON_FILE_PATH
        self.ensure_file_exists()
    
    def ensure_file_exists(self):
        """Create JSON file if it doesn't exist"""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)
    
    def get_all_todos(self):
        """Get all todos from JSON file"""
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_todos(self, todos):
        """Save todos to JSON file"""
        with open(self.file_path, 'w') as f:
            json.dump(todos, f, indent=2)
    
    def add_todo(self, title, description=''):
        """Add a new todo"""
        todos = self.get_all_todos()
        new_id = max([todo['id'] for todo in todos], default=0) + 1
        
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
    
    def get_todo_by_id(self, todo_id):
        """Get a specific todo by ID"""
        todos = self.get_all_todos()
        for todo in todos:
            if todo['id'] == todo_id:
                return todo
        return None
    
    def update_todo(self, todo_id, **kwargs):
        """Update a todo"""
        todos = self.get_all_todos()
        for todo in todos:
            if todo['id'] == todo_id:
                for key, value in kwargs.items():
                    if key in ['title', 'description', 'completed']:
                        todo[key] = value
                todo['updated_at'] = datetime.now().isoformat()
                self.save_todos(todos)
                return todo
        return None
    
    def delete_todo(self, todo_id):
        """Delete a todo"""
        todos = self.get_all_todos()
        todos = [todo for todo in todos if todo['id'] != todo_id]
        self.save_todos(todos)
        return True