from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import PetForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoption_agency'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def homepage():
    """List all pets; both available and otherwise"""

    available_pets = Pet.query.filter_by(available=True).all()
    unavailable_pets = Pet.query.filter_by(available=False).all()
    return render_template("homepage.html",available_pets=available_pets, unavailable_pets=unavailable_pets)

@app.route('/add', methods = ["GET", "POST"])
def add_pet():
    """Add new pet form"""

    form = PetForm()

    if form.validate_on_submit():
        # name= form.name.data
        # species = form.species.data
        # photo_url = form.photo_url.data
        # age = form.age.data
        # notes = form.notes.data
        # available=form.available.data
        pet_data = {key: value for key, value in form.data.items() if key != 'csrf_token'}
        
        new_pet= Pet(**pet_data)
        db.session.add(new_pet)
        db.session.commit()
        flash(f"Successfully added {new_pet.name}, the {new_pet.species}!", "success")
        return redirect("/")
    
    else:
        return render_template("add_pet_form.html", form=form)
    

    
@app.route('/pets/<int:id>', methods=["GET", "POST"])
def show_edit_pet(id):
    """Show details about a pet and provide a form to edit its information."""
    pet = Pet.query.get_or_404(id)
    form = PetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        
        db.session.commit()
        flash(f"Succesfully updated {pet.name}'s information!")
        return redirect("/")
    
    else:
        return render_template('pet_detail.html', pet=pet, form=form)


