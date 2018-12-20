import os
from flask import Flask, request, abort, url_for, redirect, session, g, render_template, flash
from models import db, User, Chatroom, Message
import json

app =  Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'chat.db')
))
app.config.from_envvar('CHAT_SETTINGS', silent=True)

db.init_app(app)

message_queue = []

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    db.drop_all()
    db.create_all()
    print('Initialized the database.')

def get_user(username):
    """Convenience method to look up a user given a username."""
    u = User.query.filter_by(username=username).first()
    return u if u else None

@app.route("/")
def default():
    return redirect(url_for("logger"))

@app.route("/login/", methods=["GET", "POST"])
def logger():
    # check if already logged in
    if "username" in session:
        flash("Already logged in!")
        return redirect(url_for("chatrooms", username=session["username"]))

    # if not, and request is via POST, try to log them in
    elif request.method == "POST":
        user = get_user(request.form["user"])
        if user and request.form["pass"] == user.password:
            session["username"] = request.form["user"]
            flash("Successfully logged in!")
            return redirect(url_for("chatrooms", username=session["username"]))
        else:
            flash("Error logging you in")

    # else, show them the login page
    return render_template("loginPage.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    # Make sure user logged in
    if "username" in session:
        flash("Already logged in!")
        return redirect(url_for("logger"))
    else:
        if request.method == "POST":
            new = User(request.form['user'], request.form['pass'])
            db.session.add(new)
            db.session.commit()
            return redirect(url_for("logger"))
        else:
            return render_template("registerPage.html")

@app.route('/chatrooms')
@app.route("/chatrooms/<username>")
def chatrooms(username=None):
    if "username" in session and session["username"] == username:
        user = get_user(username)
        room = user.chatroom_id
        if room:
            return redirect(url_for("chat", username=session["username"]))
        else:
            chatrooms = Chatroom.query.order_by(Chatroom.id.desc()).all()
            return render_template("chatrooms.html", user=user, chatrooms=chatrooms)
    else:
        abort(402)

@app.route('/chat')
@app.route('/chat/<username>')
def chat(username=None):
    if "username" in session and session["username"] == username:
        user = get_user(username)
        room = user.chatroom
        if room:
            messages = Message.query.filter_by(chatroom_id=room.id).all()
            users = User.query
            return render_template("chat.html", username=username, users=users, room=room, messages=messages)
        else:
            return redirect(url_for("chatrooms", username=session["username"]))
    else:
        abort(402)

@app.route('/makePost', methods=["POST"])
def make_post():
    user = get_user(request.form['sender'])
    room = user.chatroom
    new = Message(request.form['text'], user, room)
    db.session.add(new)
    db.session.commit()
    message_queue.append({"text" : request.form['text'], "sender" : user.username, "chatroom" : room.name})
    return "OK"

@app.route('/getPosts')
def get_posts():
    queued_messages = json.dumps(message_queue)
    del message_queue[:]
    return queued_messages

@app.route('/createRoom', methods=["GET", "POST"])
def create_room():
    # Make sure user logged in
    if "username" in session:
        if request.method == "POST":
            cur_user = get_user(session["username"])
            new = Chatroom(request.form['name'])
            cur_user.created_chats.append(new)
            db.session.add(new)
            db.session.commit()
            return redirect(url_for("chatrooms", username=session["username"]))
        else:
            return render_template("createRoom.html")
    else:
        abort(402)

@app.route('/join/<roomid>')
def join(roomid=None):
    if not roomid:
        if "username" in session:
            return redirect(url_for("chatrooms", username=session["username"]))
        else:
            return redirect(url_for("logger"))
    else:
        room_to_join = Chatroom.query.filter_by(id=roomid).first()
        user = get_user(session["username"])
        room_to_join.users.append(user)
        db.session.commit()
        return redirect(url_for("chatrooms", username=session["username"]))

@app.route('/leave/<roomid>')
def leave(roomid=None):
    if not roomid:
        if "username" in session:
            return redirect(url_for("chatrooms", username=session["username"]))
        else:
            return redirect(url_for("logger"))
    else:
        room_to_leave = Chatroom.query.filter_by(id=roomid).first()
        user = get_user(session["username"])
        room_to_leave.users.remove(user)
        db.session.commit()
        return redirect(url_for("chatrooms", username=session["username"]))

@app.route('/delete/<roomid>')
def delete(roomid=None):
    if not roomid:
        if "username" in session:
            return redirect(url_for("chatrooms", username=session["username"]))
        else:
            return redirect(url_for("logger"))
    else:
        room_to_delete = Chatroom.query.filter_by(id=roomid).first()
        db.session.delete(room_to_delete)
        db.session.commit()
        return redirect(url_for("chatrooms", username=session["username"]))

@app.route("/logout")
def unlogger():
    # if logged in, log out, otherwise show log in page
    if "username" in session:
        session.clear()
        flash("Successfully logged out!")
    else:
        flash("Not currently logged in")
    return redirect(url_for("logger"))
