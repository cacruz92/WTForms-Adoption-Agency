from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from flask_sqlalchemy import SQLAlchemy
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

with app.app_context():
    db.create_all()

@app.route('/')
def show_homepage():
    """Shows homepage with list of pet names, photos and availability"""
    pets = Pet.query.all()
    return render_template('pet_list.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    """Pet add form; handle adding"""

    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        new_pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(new_pet)
        db.session.commit()

        flash(f"Added {name} the {species}", 'success')
        return redirect('/')
    
    else:
        return render_template('add_pet_form.html', form=form)
    

@app.route("/pets/<int:pid>/edit", methods=["GET", "POST"])
def edit_pet(pid):
    """Show pet edit form and handle edit."""

    pet = Pet.query.get_or_404(pid)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        
        db.session.commit()
        flash(f"{pet.name} updated!")
        return redirect('/')

    else:
        return render_template("edit_pet_form.html", form=form, pet=pet)

if __name__ == '__main__':
    app.run()