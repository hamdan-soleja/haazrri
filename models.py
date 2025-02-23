from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin ,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    role      =db.Column(db.String(8),nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250),nullable=False)


class AttendanceStudents(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Added primary key
    attID = db.Column(db.Integer)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    rollNo = db.Column(db.String(100), nullable=False)  # Fixed `db.string`





class TeachersAttendance(UserMixin, db.Model):
    attID = db.Column(db.Integer, db.Sequence('user_id_seq', start=1000), primary_key=True)  # Primary key
    pattern = db.Column(db.String)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)  # Auto-add current date
