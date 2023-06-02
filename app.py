from sqlalchemy import inspect
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '8u3rouhfkjdsfiluh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'{self.title}'


class AddTaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DeleteTaskForm(FlaskForm):
    submit = SubmitField('Delete')


@app.route('/')
@app.route('/index')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddTaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, date=datetime.utcnow())
        db.session.add(task)
        db.session.commit()
        flash('Task added')
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    form = AddTaskForm()
    task = db.session.get(Task, task_id)
    print(task)
    if task:
        if form.validate_on_submit():
            task.title = form.title.data
            task.date = datetime.utcnow()
            db.session.commit()
            flash('Task updated')
            return redirect(url_for('index'))
        form.title.data = task.title
        return render_template('edit.html', form=form, task_id=task_id)
    flash(f'Task with id {task_id} does not exit')
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete(task_id):
    form = DeleteTaskForm()
    task = db.session.get(Task, task_id)
    if task:
        if form.validate_on_submit():
            if form.submit.data:
                db.session.delete(task)
                db.session.commit()
                flash('Task deleted')
            return redirect(url_for('index'))
        return render_template('delete.html', form=form, task_id=task_id, title=task.title)
    flash(f'Task with id {task_id} does not exit')
    return redirect(url_for('index'))


def create_db():
    with app.app_context():
        if not inspect(db.engine).has_table('task'):
            db.create_all()
            print("Database created.")
        else:
            print("Database already exists.")


if __name__ == '__main__':
    create_db()
    app.run(debug=True)
