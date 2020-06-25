from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
