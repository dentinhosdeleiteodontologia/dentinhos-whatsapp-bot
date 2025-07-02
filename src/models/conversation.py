from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    message_type = db.Column(db.String(20), default='incoming')  # incoming, outgoing
    status = db.Column(db.String(20), default='received')  # received, processed, responded
    
    def __repr__(self):
        return f'<Conversation {self.phone_number} - {self.timestamp}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'phone_number': self.phone_number,
            'message': self.message,
            'response': self.response,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'message_type': self.message_type,
            'status': self.status
        }

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)
    child_name = db.Column(db.String(100), nullable=False)
    child_age = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    preferred_period = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled
    
    def __repr__(self):
        return f'<Appointment {self.child_name} - {self.phone_number}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'phone_number': self.phone_number,
            'child_name': self.child_name,
            'child_age': self.child_age,
            'reason': self.reason,
            'preferred_period': self.preferred_period,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'status': self.status
        }

