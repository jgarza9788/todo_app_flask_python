

from flask import Flask, render_template, request, redirect, url_for

# UI/CSS
from flask_bootstrap import Bootstrap

# FORMS
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, TextAreaField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, URL

# Database
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
DEFAULT_DATE = datetime(1900, 1, 1)

import os
DIR = os.path.dirname(os.path.abspath(__file__))
print(DIR)

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + DIR + "/TaskR.db"
db = SQLAlchemy(app)


# create table

class TaskR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complete = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(50), unique=False,nullable=True) 
    description = db.Column(db.String(500), unique=False,nullable=True) 
    duedate = db.Column(db.DateTime, nullable=True) 

with app.app_context():
    db.create_all()

class TaskForm(FlaskForm):
    complete = BooleanField('Complete')
    name = StringField('Name')
    description = TextAreaField('Description')
    duedate = DateField('Due Date',default=DEFAULT_DATE)
    submit = SubmitField("Submit")

# this will decide which task to animate
anim_id = -1

@app.route("/")
def home():
    all_tasks = db.session.query(TaskR).all()
    print(all_tasks)
    print(type(all_tasks))
    return render_template('index.html', tasks=all_tasks,anim_id=anim_id)


@app.route('/add', methods=["GET", "POST"])
def add():
    anim_id = -1
    form = TaskForm()
    print(form.validate_on_submit)
    if form.validate_on_submit():
        new_task = TaskR(
            complete = form.complete.data,
            name = form.name.data,
            description = form.description.data,
            duedate = form.duedate.data
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html',form=form)



@app.route('/clicked/<int:id>', methods=["GET", "POST"])
def clicked(id):
    global anim_id 
    anim_id = id
    t = TaskR.query.get(id)
    print(t)
    print(t.id)
    print(t.name)
    if t.complete == 1:
        t.complete = 0 
    else:
        t.complete = 1
    print('Complete',t.complete)
    db.session.add(t)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    anim_id = -1
    try:
        form = TaskForm()
        tte = TaskR.query.get(id)

        if form.validate_on_submit():

            tte.complete = form.complete.data
            tte.name = form.name.data
            tte.description = form.description.data
            tte.duedate = form.duedate.data

            db.session.commit()
            return redirect(url_for('home'))
    
        else:
            print(id)
            # cafe to edit = cte
            tte = TaskR.query.get(id)

            form = TaskForm()
            form.complete.data = tte.complete
            form.name.data = tte.name
            form.description.data = tte.description
            form.duedate.data = tte.duedate

            return render_template('edit.html', form=form)
    except Exception as e:
        print('error: id: ', str(id) ,' might not exist')
        print(str(e))
    return redirect(url_for('home'))

@app.route('/delete/<int:id>', methods=["GET", "POST"])
def delete(id):
    anim_id = -1
    try:
        print(id)
        ttd = TaskR.query.get(id)
        db.session.delete(ttd)
        db.session.commit()
    except:
        print('error: id: ', str(id) ,' not deleted')
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.static_folder = 'static'
    app.debug = True
    app.run()