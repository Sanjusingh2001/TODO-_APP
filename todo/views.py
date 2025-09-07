from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import TodoManager

def index(request):
    """Render the main todo page"""
    return render(request, 'todo/index.html')

@csrf_exempt
def todo_list_api(request):
    """API endpoint to get all todos or create a new todo"""
    todo_manager = TodoManager()
    
    if request.method == 'GET':
        todos = todo_manager.get_all_todos()
        return JsonResponse({'todos': todos})
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title', '').strip()
            description = data.get('description', '').strip()
            
            if not title:
                return JsonResponse({'error': 'Title is required'}, status=400)
            
            new_todo = todo_manager.add_todo(title, description)
            return JsonResponse({'todo': new_todo}, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

@csrf_exempt
@require_http_methods(["PUT", "DELETE"])
def todo_detail_api(request, todo_id):
    """API endpoint to update or delete a specific todo"""
    todo_manager = TodoManager()
    
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            updated_todo = todo_manager.update_todo(todo_id, **data)
            
            if updated_todo:
                return JsonResponse({'todo': updated_todo})
            else:
                return JsonResponse({'error': 'Todo not found'}, status=404)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    elif request.method == 'DELETE':
        todo = todo_manager.get_todo_by_id(todo_id)
        if todo:
            todo_manager.delete_todo(todo_id)
            return JsonResponse({'message': 'Todo deleted successfully'})
        else:
            return JsonResponse({'error': 'Todo not found'}, status=404)