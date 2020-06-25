from datetime import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app, resources={r'/*': {'origins': '*'}})

class Priority(db.Model):
	priority_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	tasks = db.relationship('Task', back_populates='priority')

class Task(db.Model):
	task_id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(200), nullable=False)
	priority_id = db.Column(db.Integer, db.ForeignKey('priority.priority_id'), default=2)
	priority = db.relationship('Priority', back_populates='tasks')
	created_at = db.Column(db.DateTime, default=datetime.now)

class PrioritySchema(ma.Schema):
	class Meta:
		fields = ('priority_id', 'name')

class TaskSchema(ma.Schema):
	class Meta:
		fields = ('task_id', 'description', 'priority_id', 'priority', 'created_at')
		datetimeformat='%Y-%m-%d %H:%M'
	priority = ma.Nested(PrioritySchema)

priority_schema = PrioritySchema()
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# show all tasks
@app.route('/task', methods=['GET'])
def get_tasks():
	tasks = Task.query.all()
	return jsonify(tasks_schema.dump(tasks))

# show task by id
@app.route('/task/<task_id>', methods=['GET'])
def get_task(task_id):
	task = Task.query.get(task_id)
	return task_schema.jsonify(task)

def validate_post_data(req_data):
	if not req_data:
		return 'Missing request data'
	if 'description' not in req_data or \
		not req_data['description'] or len(str(req_data['description']))>200:
		return 'Invalid or missing description'
	if 'priority_id' in req_data and not Priority.query.get(req_data['priority_id']):
		return 'Invalid priority_id'		

# create new task 
@app.route('/task', methods=['POST'])
def add_task():
	req_data = request.json
	error = validate_post_data(req_data)
	if error:
		return error, 400
	description = str(req_data['description'])
	priority_id = req_data.get('priority_id')
	new_task = Task(description=description, priority_id=priority_id)
	db.session.add(new_task)
	db.session.commit()
	return task_schema.jsonify(new_task)	

def validate_put_data(task_id, req_data):
	if not Task.query.get(task_id):
		return f'task_id={task_id} not found'
	if not req_data :
		return 'Missing request data'
	if 'description' in req_data and \
		(not req_data['description'] or len(str(req_data['description']))>200):
		return 'Invalid description'
	if 'priority_id' in req_data and not Priority.query.get(req_data['priority_id']):
		return 'Invalid priority_id'

# update task
@app.route('/task/<task_id>', methods=['PUT'])
def update_task(task_id):
	req_data = request.json
	error = validate_put_data(task_id, req_data)
	if error:
		return error, 400
	task = Task.query.get(task_id)
	task.description = str(req_data.get('description', task.description))
	task.priority_id = req_data.get('priority_id', task.priority_id)
	db.session.commit()		
	return task_schema.jsonify(task)
	
# delete task
@app.route('/task/<task_id>', methods=['DELETE'])
def delete_task(task_id):
	task = Task.query.get(task_id)
	if not task:
		return f'task_id={task_id} not found', 400
	db.session.delete(task)
	db.session.commit()
	return task_schema.jsonify(task)