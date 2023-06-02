from sqlalchemy import inspect
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8u3rouhfkjdsfiluh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
def create_db():
    with app.app_context():
        if not inspect(db.engine).has_table('task'):
            db.create_all()
            print("Database created.")
        else:
            print("Database already exists.")

from routes import *

if __name__ == '__main__':
    create_db()
    app.run(debug=True)
