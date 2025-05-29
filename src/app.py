from flask import Flask, request, jsonify, render_template_string
import os
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Simple task storage
tasks = [
    {"id": 1, "title": "Setup CI/CD Pipeline", "completed": False, "created": "2025-5-20"},
    {"id": 2, "title": "Write Tests", "completed": True, "created": "2025-5-20"}
]

# Home Page Template
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Task Management API</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .task { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }
        .completed { background: #d4edda; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Task Management API</h1>
        <p><strong>Version:</strong> 1.2.0 | <strong>Status:</strong> ✅ Healthy</p>
        
        <h3>API Endpoints:</h3>
        <ul>
            <li><code>GET /tasks</code> - Get all tasks</li>
            <li><code>POST /tasks</code> - Create new task</li>
            <li><code>GET /health</code> - Health check</li>
        </ul>

        <h3>Current Tasks:</h3>
        {% for task in tasks %}
        <div class="task {{ 'completed' if task.completed else '' }}">
            <strong>{{ task.title }}</strong><br>
            Status: {{ 'Completed' if task.completed else 'Pending' }}<br>
            Created: {{ task.created }}
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE, tasks=tasks)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks, "count": len(tasks)})

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    new_task = {
        "id": len(tasks) + 1,
        "title": data['title'],
        "completed": data.get('completed', False),
        "created": datetime.now().strftime("%Y-%m-%d")
    }
    tasks.append(new_task)
    return jsonify({"task": new_task}), 201

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
