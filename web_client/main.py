import sys

from flask import Flask, render_template

from web_client import forms

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_penis'

@app.route('/')
def home():
    return render_template('penis.html', big_penis=False)

@app.route('/signup')
def signup():
    form = forms.SignUpForm()
    return render_template('signup.html', form=form)




if __name__ == '__main__':
    app.run()