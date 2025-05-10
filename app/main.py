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
