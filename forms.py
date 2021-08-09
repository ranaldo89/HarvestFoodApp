from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SelectField,IntegerField, FloatField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed

class NewMeals(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    prepTime=IntegerField('Prep Time',validators=[DataRequired()])
    fat=IntegerField('Fat',validators=[DataRequired()])
    carbohydrates=IntegerField('Carbohydrates',validators=[DataRequired()])
    protein=FloatField('Protein',validators=[DataRequired()])
    calories=FloatField('Calories',validators=[DataRequired()])
    image = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'Images only!'])])