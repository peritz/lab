from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<h1>Hello, World!</h1>"

@app.route('/user/<username>')
def get_user(username):
    return render_template('user.html', username=username)

@app.route('/basic')
def basic():
    return render_template('basic.html')

if __name__ == '__main__':
    app.run(debug=True)
