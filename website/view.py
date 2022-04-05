from flask import Blueprint,render_template,flash,redirect,url_for,request
from flask_login import current_user,login_required
from .models import Notes
from . import db
view = Blueprint("view", __name__)


@view.route("/",methods=["GET","POST"])
@login_required
def home():
    if request.method == "POST":
        notes = request.form.get("note")
        if len(notes) <1:
            flash("Note must be a character", category="success")
        else:
            user = Notes(data = notes, user_id = current_user.id)
            db.session.add(user)
            db.session.commit()
            flash("Note successfully added!!", category= "success")
    return render_template("notes.html",user = current_user)


@view.route("/delete/<int:id>")
def delete(id):
    v = Notes.query.get(id)
    db.session.delete(v)
    db.session.commit()
    flash("Note successfuly deleted!!",category="success")
    return redirect(url_for("view.home"))


@view.route("/update/<int:id>", methods=["GET","POST"])
def Update(id):
    v = Notes.query.filter_by(id=id).first()
    if request.method == "POST":
        data=request.form.get("note")

        v.data=data
        db.session.add(v)
        db.session.commit()
        flash("Note updated",category="success")
        return redirect(url_for("view.home"))



    return render_template("update.html", v=v, user= current_user,)

