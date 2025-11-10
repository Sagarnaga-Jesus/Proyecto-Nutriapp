from flask import Flask,render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = '1q2w3e4r5t6y7u8i9o0pp0o9i8u7y6t5r4e3w2q1'
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route('/')
def index():
    return render_template('buscador.html')

if __name__ == '__main__':
    app.run(debug=True)