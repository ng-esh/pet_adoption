from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField
from wtforms.validators import InputRequired, Optional, URL, AnyOf

ages = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
        11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 26, 27, 28, 19, 30]

class PetForm(FlaskForm):
    """Form for adding a pet"""

    name = StringField("Pet Name", 
                       validators=[InputRequired(message="pet name cant be blank")])
    
    species = StringField("species", 
                         validators =[InputRequired(),
                                      AnyOf(["cat", "dog", "porcupine"], message = "pet species must be either cat, dog or porcupine")])
    
    photo_url = TextAreaField ("Image Url", 
                               validators =[URL(), Optional()])
    
    age = SelectField("Age", choices=[(age, age) for age in ages], coerce=int)

    notes = TextAreaField ("Anything of note", 
                           validators =[Optional()]) 
    
    available = BooleanField("Pet Availability")