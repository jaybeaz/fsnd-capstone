import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Person
'''
class Person(db.Model):  
  __tablename__ = 'People'

  id = Column(db.Integer, primary_key=True)
  name = Column(String)
  catchphrase = Column(String)

  def __init__(self, name, catchphrase=""):
    self.name = name
    self.catchphrase = catchphrase

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'catchphrase': self.catchphrase}
  
class Movies(db.Model):
  __tablename__ = 'Movies'

  id = Column(db.Integer, primary_key=True)
  title = Column(db.String(120))
  release_date = db.Column(db.Date)

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
      db.session.commit()

  def delete(self):
      db.session.delete(self)
      db.session.commit() 

  def format(self):
    return {
      'movie': self.id, 
      'title': self.title, 
      'release_date': self.release_date
      }

class Actors(db.Model):
  __tablename__ = 'Actors'

  id = Column(db.Integer, primary_key=True)
  name = Column(db.String(120))
  age = db.Column(db.Integer)
  gender = db.Column(db.String(20))

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
      db.session.commit()

  def delete(self):
      db.session.delete(self)
      db.session.commit()  

  def format(self):
    return {
      'id': self.id,
      'name': self.name, 
      'age': self.age,
      'gender': self.gender
      }
