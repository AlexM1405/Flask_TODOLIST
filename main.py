from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_login import login_required, current_user
import unittest
from os import urandom
from app import create_app
from db import database
from app.firestore_service import get_users, get_todos, put_todo, delete_todo, update_todo

from app.forms import TodoForm, DeleteTodoForm, UpdateTodoForm

app = create_app()
db = database()

app = Flask(__name__)

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config["SECRET_KEY"] = urandom(16)

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestResult().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect("/hello"))
    session["user_ip"] = user_ip

    return response

@app.route('/hello', methods=["GET", "POST"])
@login_required
def hello():
    user_ip = session.get("user_ip")
    username = current_user.id
    todo_form = TodoForm()
    Delete_form = DeleteTodoForm()
    update_form = UpdateTodoForm()
    
    context = {
        "user_ip": user_ip,
        "todoList": get_todos(user_id=username),
        "username":username,
        "todo_form":todo_form,
        "Delete_form":Delete_form,
        "update_form":update_form
        
    }

    if todo_form.validate_on_submit():
        put_todo(user_ip=username,description=todo_form.description.data)
    
        flash('Your task has been added!','success')
        return redirect(url_for('hello'))
       
    return render_template("hello.html", **context)

@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)

    return redirect(url_for('hello'))


@app.route('/todos/update/<todo_id>/<done>', methods=['POST'])
def update(todo_id, done):
    user_id = current_user.id

    update_todo(user_id=user_id, todo_id=todo_id, done=done)

    return redirect(url_for('hello'))



