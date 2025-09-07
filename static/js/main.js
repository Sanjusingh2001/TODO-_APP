
class TodoApp {
    constructor() {
        this.apiUrl = '/api/todos/';
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadTodos();
    }

    bindEvents() {
        const form = document.getElementById('todoForm');
        form.addEventListener('submit', (e) => this.handleAddTodo(e));
    }

    async loadTodos() {
        try {
            const container = document.getElementById('todoContainer');
            container.innerHTML = '<div class="loading">Loading todos...</div>';

            const response = await fetch(this.apiUrl);
            const data = await response.json();

            if (data.todos && data.todos.length > 0) {
                this.renderTodos(data.todos);
            } else {
                container.innerHTML = '<div class="no-todos">No todos yet. Add your first todo above!</div>';
            }
        } catch (error) {
            console.error('Error loading todos:', error);
            document.getElementById('todoContainer').innerHTML = 
                '<div class="error">Error loading todos. Please try again.</div>';
        }
    }

    renderTodos(todos) {
        const container = document.getElementById('todoContainer');
        
        const todosHtml = todos.map(todo => `
            <div class="todo-item ${todo.completed ? 'completed' : ''}" data-id="${todo.id}">
                <div class="todo-title">${this.escapeHtml(todo.title)}</div>
                ${todo.description ? `<div class="todo-description">${this.escapeHtml(todo.description)}</div>` : ''}
                <div class="todo-meta">
                    Created: ${this.formatDate(todo.created_at)} 
                    ${todo.updated_at !== todo.created_at ? `| Updated: ${this.formatDate(todo.updated_at)}` : ''}
                </div>
                <div class="todo-actions">
                    <button class="btn-${todo.completed ? 'incomplete' : 'complete'}" 
                            onclick="todoApp.toggleComplete(${todo.id}, ${!todo.completed})">
                        ${todo.completed ? 'Mark Incomplete' : 'Mark Complete'}
                    </button>
                    <button class="btn-delete" onclick="todoApp.deleteTodo(${todo.id})">
                        Delete
                    </button>
                </div>
            </div>
        `).join('');

        container.innerHTML = todosHtml;
    }

    async handleAddTodo(e) {
        e.preventDefault();
        
        const title = document.getElementById('title').value.trim();
        const description = document.getElementById('description').value.trim();

        if (!title) {
            alert('Please enter a title for your todo');
            return;
        }

        try {
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title: title,
                    description: description
                })
            });

            if (response.ok) {
                document.getElementById('todoForm').reset();
                this.loadTodos();
            } else {
                const error = await response.json();
                alert('Error: ' + (error.error || 'Failed to add todo'));
            }
        } catch (error) {
            console.error('Error adding todo:', error);
            alert('Error adding todo. Please try again.');
        }
    }

    async toggleComplete(todoId, completed) {
        try {
            const response = await fetch(`${this.apiUrl}${todoId}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    completed: completed
                })
            });

            if (response.ok) {
                this.loadTodos();
            } else {
                alert('Error updating todo');
            }
        } catch (error) {
            console.error('Error updating todo:', error);
            alert('Error updating todo. Please try again.');
        }
    }

    async deleteTodo(todoId) {
        if (!confirm('Are you sure you want to delete this todo?')) {
            return;
        }

        try {
            const response = await fetch(`${this.apiUrl}${todoId}/`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.loadTodos();
            } else {
                alert('Error deleting todo');
            }
        } catch (error) {
            console.error('Error deleting todo:', error);
            alert('Error deleting todo. Please try again.');
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.todoApp = new TodoApp();
});