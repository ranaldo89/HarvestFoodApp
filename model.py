"""Models and database functions"""
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SelectField,IntegerField, FloatField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed


# connection to the PostgreSQL database
db = SQLAlchemy()

############################## Model definitions ###############################


class User(db.Model):
    """User of website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    pw = db.Column(db.String(100), nullable=False)
    bday = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(1), nullable=False)

    def __init__(self, fname, lname, email, pw, bday, gender):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.pw = pw
        self.bday = bday
        self.gender = gender

    def getuserid(self):
        return self.user_id


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={} fname={} lname={}>".format(self.user_id, self.fname, self.lname)



class Meals(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150))
    prepTime = db.Column(db.Integer)
    fat=db.Column(db.Integer)
    carbohydrates = db.Column(db.Integer)
    protein = db.Column(db.Float(10))
    calories= db.Column(db.Float(50))
    photo = db.Column(db.String(250))
    def __init__(self, title, prepTime, fat,carbohydrates,protein,calories,photo):
        self.title = title
        self.prepTime = prepTime
        self.fat = fat
        self.carbohydrates=carbohydrates
        self.protein=protein
        self.calories=calories
        self.photo=photo

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return "<Recipe id={} foodName={} description={}>".format(self.id, self.title, self.prepTime )



class Recipe(db.Model):
    """Saved recipe on website (from Spoonacular API)."""

    __tablename__ = "recipes"

    recipe_id = db.Column(db.Integer, primary_key=True)
    num_saved = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(250), nullable=False)
    prep_time = db.Column(db.Integer, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    carbohydrates = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Recipe recipe_id={} title={} num_saved={}>".format(self.recipe_id, self.title, self.num_saved)



class Plan(db.Model):
    """Saved meal plans on website."""

    __tablename__ = "plans"

    plan_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
    start = db.Column(db.Date, nullable=False)
    order_status = db.Column(db.String(100), nullable=False)

    recipes = db.relationship("Recipe", secondary="assoc", backref="plans")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Plan plan_id={} user_id={} start={}>".format(self.plan_id, self.user_id, self.start)


class PlanRecipe(db.Model):
    """User of website."""

    __tablename__ = "assoc"

    assoc_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'), index=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), index=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Assoc assoc_id={} user_id={} recipe_id={}>".format(self.assoc_id, self.user_id, self.recipe_id)





############################## Helper Functions ###############################

def connect_to_db(app, db_uri='postgresql://postgres:00000@localhost/harvest'):
    

    """Connect the database to the Flask app."""
   
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from app import app
    connect_to_db(app)
    db.create_all()
    print ("Connected to DB")


