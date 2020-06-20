from flask import Flask, render_template, request
from web_client.forms import LoadUserForm
from wtforms import StringField, TextField
from classes import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_penis'

@app.route('/', methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        user = User(username=username)
        # user.load()
        return render_template('load_user.html', f_name=user.f_name)


    return render_template('load_user.html', f_name='')


if __name__ == '__main__':
    app.run()