
from flask import render_template, session, redirect, flash,url_for
from . import auth
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm
from app.firestore_service import get_user, user_put
from app.models import UserModel, UserData

@auth.route("/login", methods=["GET", "POST"])
def login():
    loginForm = LoginForm()
    context = {
        "form": LoginForm()
    }
    if loginForm.validate_on_submit():
        username = loginForm.username.data
        password = loginForm.password.data

        user_doc = get_user(username)
        if user_doc.to_dict() is not None:

            if check_password_hash (user_doc.to_dict() ["password"], password):
            
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)
                flash("Welcome Back")
                redirect(url_for("hello"))
            else:
                flash("Invalid Password")
        else:
            flash("User Not Found")

        return redirect(url_for("index"))
    
    return render_template("login.html", **context )


@auth.route("signup", methods = ["GET", "POST"])
def signup():
  SignUpForm = LoginForm()
  context = {
     "sigUpform" : SignUpForm
  }
  if SignUpForm.validate_on_submit():
      username = SignUpForm.username.data
      password = SignUpForm.password.data

      user_doc = get_user(username)

      if user_doc.to_dict() is None:
         hashed_pw = generate_password_hash(password)
         user_data = UserData(username, hashed_pw)
         user_put(user_data)

         user = UserModel(user_data)
         login_user(user)
         flash ("Sign Up Successful! Welcome to the site.")
         return redirect(url_for('hello'))
      
      else:
          flash("Username already exists")
  return render_template("signup.html", **context )


@auth.route("logout")
@login_required
def logout():
    logout_user()
    flash("Logged out Successfully!")

    redirect(url_for("auth.login"))