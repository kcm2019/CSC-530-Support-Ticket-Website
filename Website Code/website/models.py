from . import db #imports from website our db object
from flask_login import UserMixin #Helps log users in
from sqlalchemy.sql import func

#Creating Database Model 
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #Automatically adds the date for us
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #Foreign key is the user.id that created the note

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #ID will be incremented on its own
    email = db.Column(db.String(150), unique=True) #No user can have the same email as another user that exists
    password = db.Column(db.String(150))
    first_Name = db.Column(db.String(150))
    notes = db.relationship('Note') #tells Flask and SQL to add to this relationship the note.id

