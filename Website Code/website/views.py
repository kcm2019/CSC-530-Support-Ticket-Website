from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import jsonify

#This application has a bunch of URLs defined here so that we can have our views defined in several files and not a single one
#This is what Blueprints allows us to do
views = Blueprint('views', __name__)

#Decorator, calls on the function when this route is hit
@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    notes = Note.query.all()
    if (current_user.admin_access == True):
        """if request.method == 'POST': # and request.form["note-submit"]
            note = request.form.get('note')

            if len(note) < 1:
                flash('Comment is too short', category='error')
            else:
                new_note = Note(data=note, user_id=current_user.id, status="Open")
                db.session.add(new_note)
                db.session.commit()
                flash('Incident Added!', category='success') """
        if request.method == 'POST': # and request.form["note-edit"]
            note_id = request.form.get('note_id')
            admin_comments = request.form.get("admin_comments")
            status = request.form.get("note_status")
            note = Note.query.filter_by(id=note_id).first()
            print("*****NOTE EDITING IN ADMIN VIEW******")
            print(note)
            print(type(note))
            if len(admin_comments) < 1:
                flash("Comment is too short", category='error')
            #elif Note.query.filter_by(id=note_id).first() != note_id: #Checks if note exists
                #flash("Incident Does Not Exist", category='error')
            #elif status != "Open" or status != "Closed" or status != "In Progress":
                #flash("Status must be Open, Closed, or In Progress", category='error')
            else:
                updated_note = Note(id=note_id, data=note.data, user_id=note.user_id, admin_notes=admin_comments, status=status)

                db.session.delete(note)
                db.session.commit()

                db.session.add(updated_note)
                db.session.commit()
                flash('Incident Edited!', category='success')
        return render_template("admin.html", user=current_user, notes=notes)
    else: 
        if request.method == 'POST':
            note = request.form.get('note')

            if len(note) < 1:
                flash('Note is too short', category='error')
            else:
                new_note = Note(data=note, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Note Added!', category='success')
        return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    #Prevents Users who do not own the note from deleting it
    if note:
        if note.user_id == current_user.id or current_user.admin_access == True:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


