from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Round
from . import db, validator, external, format
import json

ROUND_DATA = {}
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
    global ROUND_DATA
    if request.method == 'POST':
        if request.form.get('_method') != 'PATCH':
            # Gets the part-1 round data 
            ROUND_DATA = post_score_1()
            if not ROUND_DATA:
                flash("Course not found, please check spelling and try again", category="error")
                return render_template("post_score.html", user=current_user)
            ROUND_DATA["tee_data"] = format.format_tee_data(ROUND_DATA.pop("tee_rating_data"), ROUND_DATA["front_or_back"])
            return render_template("post_score_2.html", user=current_user, tees=list(ROUND_DATA["tee_data"].keys()))
        else:
            return render_template("confirm_round.html", user=current_user)
            # new_round = Round(
            #     course=course,
            #     tees=tees,
            #     front_or_back=front_or_back,
            #     slope=slope,
            #     course_rating=course_rating,
            #     date_played=date,
            #     score=score,
            #     attestor=attestor,
            #     user_id=current_user.id
            # )  
            # db.session.add(new_round) #adding the note to the database 
            # db.session.commit()
            # flash('Round added!', category='success')
    return render_template("post_score.html", user=current_user)


def post_score_1():
    date = request.form.get('date')
    course = request.form.get('course')
    state = request.form.get("state") 
    front_or_back = request.form.get('front_or_back')

    data = {
        "course": course,
        "state": state,
        "front_or_back": front_or_back,
        "date": date,
    }
    if validator.validate_posted_score_1(data):
        course_id = external.get_course_data(course, state)
        if not course_id:
            return None
        data.update({
            "course_id": course_id,
            "tee_rating_data": external.get_tee_ratings(course_id)
        })
    return data

# @views.route('/post-score-2', methods=['GET', 'POST'])
# @login_required
def post_score_2():
    return render_template("post_score_2.html", user=current_user)


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
