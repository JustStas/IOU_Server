from flask import Flask, render_template
from forms import SignUpForm

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('penis.html', big_penis=False)



if __name__ == '__main__':
    app.run()