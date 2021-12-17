#!/usr/bin/python3

from flask import Flask, redirect, render_template, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager , UserMixin , login_required ,login_user, logout_user,current_user
from datetime import timedelta
import random

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['SECRET_KEY']='flaskgame'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.permanent_session_lifetime = timedelta(minutes=30)
db = SQLAlchemy(app)

questions = [
    {
        "id": "1",
        "question": "What is the Capital of Nepal?",
        "answers": ["a) Dharan", "b) Pokhara", "c) Kathmandu"],
        "correct": "c) Kathmandu"
    },
    {
        "id": "2",
        "question": "What is the square root of Pi?",
        "answers": ["a) 1.7724", "b) 1.6487", "c) 1.7872"],
        "correct": "a) 1.7724"
    },
    {
        "id": "3",
        "question": "What is the Capital of England?",
        "answers": ["a) Liverpool", "b) London", "c) Winchester"],
        "correct": "b) London"
    },
    {
        "id": "4",
        "question": "What is the smallest planet in our solar system?",
        "answers": ["a) Mercury", "b) Mars", "c) Saturn"],
        "correct": "a) Mercury"
    },
    {
        "id": "5",
        "question": "Who is the CEO of Facebook?",
        "answers": ["a) Steve Jobs", "b) Mark Zuckerberg", "c) Bill Gates"],
        "correct": "b) Mark Zuckerberg"
    },
    {
        "id": "6",
        "question": "How many times has Brazil won FIFA World Cup?",
        "answers": ["a) Three", "b) Zero", "c) Five"],
        "correct": "c) Five"
    },
    {
        "id": "7",
        "question": "Who is known as first programmer?",
        "answers": ["a) John Ambrose Fleming", "b) Charles Babbage", "c) Ada Lovelace"],
        "correct": "c) Ada Lovelace"
    },
    {
        "id": "8",
        "question": "The value of x + x(xx) when x = 2 is:",
        "answers": ["a) 10", "b) 16", "c) 36"],
        "correct": "a) 10"
    },
    {
        "id": "9",
        "question": "How many human players are there on each side in a Basketball match?",
        "answers": ["a) Three", "b) Five", "c) Seven"],
        "correct": "b) Five"
    },
    {
        "id": "10",
        "question": "What is the height of Mt. Everest?",
        "answers": ["a) 8,859 metres", "b) 8,848.86 metres", "c) 8,846.86 metres"],
        "correct": "b) 8,848.86 metres"
    },
]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
        self.result = result


@app.route('/', methods=['GET','POST'])
def index():
    if session.get('logged_in'):
        if request.method == 'GET':
            return render_template("home.html", data=questions)
        else:
            result = 0
            total = 0
            score = 0
            for question in questions:
                if request.form[question.get('id')] == question.get('correct'):
                    result += 1
                    score = result * 5
                total += 1
            return render_template('results.html', total=total, result=result, score=score)
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(User(email=request.form['email'], username=request.form['username'], password=request.form['password']))
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('register.html', message="User Already Exists")
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        u = request.form['username']
        p = request.form['password']
        data = User.query.filter_by(username=u, password=p).first()
        if data is not None:
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('login.html', message="Incorrect Details")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))


if __name__ == "__main__":
    db.create_all()
    app.run()