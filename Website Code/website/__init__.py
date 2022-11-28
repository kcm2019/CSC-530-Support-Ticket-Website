from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#Databse Object
db = SQLAlchemy()
DB_NAME = 'database.db'


#This __init__.py makes the website folder a python package and allows us to imoprt it in our main
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'THIS IS THE SECRET KEY FOR THE APP' #can be anything you want but you want to hide this
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #Telling flask where the databse is located
    db.init_app(app) #initializing database with the app\

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #Creating the database and importing the tables
    from .models import User, Note

    #create_database(app)

    #https://stackoverflow.com/questions/73968584/flask-sqlalchemy-db-create-all-got-an-unexpected-keyword-argument-app
    with app.app_context(): 
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#def create_database(app):
#    if not path.exists('website/' + DB_NAME):
#        db.create_all(app=app)
#        print('Created Databse!')

