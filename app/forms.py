from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Name for the User", validators=DataRequired())
    password = PasswordField("Password for the user", validators=DataRequired())
    submit = SubmitField("Sent")


class TodoForm(FlaskForm):
    description = StringField("Description", validators=[DataRequired()])
    submit = SubmitField("Create")


class DeleteTodoForm(FlaskForm):
    submit = SubmitField("Delete")

class UpdateTodoForm(FlaskForm):
    submit = SubmitField("Update")