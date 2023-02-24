from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Round
from . import db
from . import validator
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/post-score', methods=['GET', 'POST'])
@login_required
def post_score():
    if request.method == 'POST': 
        #Gets the round from the HTML
        course = request.form.get('course') 
        tees = request.form.get('tees')
        front_or_back = request.form.get('front_or_back')
        slope = request.form.get('slope')
        course_rating = request.form.get('course_rating')
        date = request.form.get('date')
        score = request.form.get('score')
        attestor = request.form.get('attestor')

        data = {
            "Course": course,
            "Tees": tees,
            "Front/Back": front_or_back,
            "Slope": slope,
            "Course Rating": course_rating,
            "Date": date,
            "Score": score,
            "Attestor": attestor
        }

        if validator.validate_posted_score(data):
            new_round = Round(
                course=course,
                tees=tees,
                front_or_back=front_or_back,
                slope=slope,
                course_rating=course_rating,
                date_played=date,
                score=score,
                attestor=attestor,
                user_id=current_user.id
            )  
            db.session.add(new_round) #adding the note to the database 
            db.session.commit()
            flash('Round added!', category='success')

    return render_template("post_score.html", user=current_user) 


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
