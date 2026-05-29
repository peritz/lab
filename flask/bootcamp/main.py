from flask import Flask, render_template, flash, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)

app.config["SECRET_KEY"] = "thisismysecretkey"

@app.route('/')
def hello_world():
    return "<h1>Hello, World!</h1>"

@app.route('/user/<username>')
def get_user(username):
    return render_template('user.html', username=username)

@app.route('/basic')
def basic():
    return render_template('basic.html')

@app.route('/basic/flash')
def basic_flash():
    flash("Here is some information about a message!")
    return redirect(url_for("basic"))

class UserForm(FlaskForm):
    name = StringField("Name")
    email = StringField("Email")
    submit = SubmitField("Submit")

@app.route('/form', methods=["GET", "POST"])
def form():
    name = False
    email = False
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        email = form.email.data
        form.email.data = ""
    return render_template("form.html", form=form, name=name, email=email)

if __name__ == '__main__':
    app.run(debug=True)
