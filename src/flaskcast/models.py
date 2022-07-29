#from flaskcast import db
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Actor(db.Model):
    __tablename__ = 'actors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def __repr__(self):
        return f"<id: ${self.id} - actor's name: ${self.name} - age: ${self.age}> - gender: ${self.gender}"


class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    actors = db.relationship(
        'Actor',
        secondary = 'movie_cast',
        backref = db.backref('cast', lazy=True)
    )

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def __repr__(self):
        return f'<id: ${self.id} - movie: ${self.title} - release date: ${self.release_date}>'

movie_cast = db.Table(
    'movie_cast',
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True) 
)