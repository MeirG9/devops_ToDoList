from flask import Flask, request, jsonify
import redis

app = Flask(__name__)

r = redis.Redis(host='redis', port=6379, db=0)

def get_next_todo_id():

    next_id = r.get('next_todo_id')
    if next_id is None:
        next_id = 1  
    else:
        next_id = int(next_id)
    r.set('next_todo_id', next_id + 1)  
    return next_id

@app.route('/todo', methods=['POST'])
def add_todo_list():
    tasks = request.json.get('tasks')  

    if not tasks or not isinstance(tasks, list):
        return jsonify({'message': 'Tasks must be provided as a list'}), 400

    todo_id = get_next_todo_id()  
    r.set(todo_id, str(tasks))

    return jsonify({
        'id': todo_id,
        'message': 'To-Do List saved successfully'
    }), 201

@app.route('/todo/<todo_id>', methods=['DELETE'])
def delete_todo_list(todo_id):
    r.delete(todo_id)
    return jsonify({
        'message': 'To-Do List deleted'
    })

@app.route('/todos', methods=['GET'])
def get_all_todos():
    keys = r.keys(pattern='*')  
    todos = {}

    for key in keys:
        try:
            int_key = int(key)
            value = r.get(key).decode('utf-8')
            todos[int_key] = value
        except:
            continue  

    return jsonify(todos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
