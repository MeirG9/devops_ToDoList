from flask import Flask, request, jsonify
import redis
import json

app = Flask(__name__)

# Connect to Redis container
r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

def get_next_todo_id():
    """
    Increments and returns the next available To-Do ID.
    """
    next_id = r.get('next_todo_id')
    if next_id is None:
        next_id = 1
    else:
        next_id = int(next_id)
    r.set('next_todo_id', next_id + 1)
    return next_id

@app.route('/', methods=['GET'])
def index():
    """
    Welcome message and documentation summary for the API root.
    """
    return jsonify({
        "message": "Welcome to the To-Do List API",
        "version": "1.0",
        "description": "This RESTful API allows you to manage multiple to-do lists using JSON over HTTP.",
        "base_url": "http://localhost:5000",
        "endpoints": {
            "POST /todo": "Create a new To-Do list",
            "GET /todo/<id>": "Retrieve a specific To-Do list",
            "DELETE /todo/<id>": "Delete a specific To-Do list",
            "GET /todos": "Retrieve all To-Do lists"
        },
        "example_request": {
            "POST /todo": {
                "content-type": "application/json",
                "body": {
                    "tasks": ["Buy groceries", "Finish assignment", "Walk the dog"]
                }
            }
        },
        "example_response": {
            "201 Created": {
                "id": 1,
                "message": "To-Do List saved successfully"
            }
        },
        "note": "This API only supports JSON. See README.md for full documentation."
    }), 200

@app.route('/todo', methods=['POST'])
def add_todo_list():
    """
    Create a new To-Do list with multiple tasks.
    """
    tasks = request.json.get('tasks')
    if not tasks or not isinstance(tasks, list):
        return jsonify({'message': 'Tasks must be provided as a list'}), 400

    todo_id = get_next_todo_id()
    r.set(f"todo:{todo_id}", json.dumps(tasks))

    return jsonify({
        'id': todo_id,
        'message': 'To-Do List saved successfully'
    }), 201

@app.route('/todo/<todo_id>', methods=['GET'])
def get_single_todo(todo_id):
    """
    Retrieve a single To-Do list by its ID.
    """
    value = r.get(f"todo:{todo_id}")
    if not value:
        return jsonify({'message': 'To-Do not found'}), 404

    return jsonify({
        'id': todo_id,
        'tasks': json.loads(value)
    }), 200

@app.route('/todo/<todo_id>', methods=['DELETE'])
def delete_todo_list(todo_id):
    """
    Delete a To-Do list by its ID.
    """
    result = r.delete(f"todo:{todo_id}")
    if result == 0:
        return jsonify({'message': 'To-Do not found'}), 404

    return jsonify({'message': 'To-Do List deleted'}), 200

@app.route('/todos', methods=['GET'])
def get_all_todos():
    """
    Retrieve all existing To-Do lists.
    """
    keys = r.keys(pattern='todo:*')
    todos = {}

    for key in keys:
        todo_id = key.split(":")[1]
        try:
            tasks = json.loads(r.get(key))
            todos[todo_id] = tasks
        except (ValueError, json.JSONDecodeError):
            continue

    return jsonify(todos), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
