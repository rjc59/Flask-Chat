from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

created = db.Table('created',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('chatroom_id', db.Integer, db.ForeignKey('chatroom.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(24), nullable=False)
    chatroom_id = db.Column(db.Integer, db.ForeignKey('chatroom.id'))
    created_chats = db.relationship('Chatroom', secondary=created, backref=db.backref('creator', lazy='dynamic'))
    messages = db.relationship('Message', backref='sender', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Chatroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False)
    users = db.relationship('User', backref='chatroom', lazy='dynamic')
    messages = db.relationship('Message', backref='chatroom', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Chatroom {}'.format(self.id)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    chatroom_id = db.Column(db.Integer, db.ForeignKey('chatroom.id'))

    def __init__(self, text, sender, chatroom):
        self.text = text
        self.sender_id = sender.id
        self.chatroom_id = chatroom.id
