from flask import Blueprint, render_template, request, flash,url_for, redirect
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import  login_user, logout_user, login_required,current_user
from random import randint

authe = Blueprint("authe", __name__)
Number=""
def calc():
    global Number
    Number = str(randint(0,20)) +"+"+ str(randint(0,20))
calc()


@authe.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        num = request.form.get("number")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password) and eval(Number) == int(num):
                flash("Loging succesfull!",category="success")
                login_user(user)
                return redirect(url_for("view.home"))
            elif eval(Number) != int(num):
                #calc()
                flash("wrong.", category="error")
            else:
                #calc()
                flash("Incorrect-password.", category="error")
        else:
            #calc()
            flash("Email does not found.", category="error")
    calc()
    return render_template("login.html",user=current_user,text =Number)


@authe.route("/logout")
@login_required
def logout():
    logout_user()
    #calc()
    return  redirect(url_for("authe.login"))


@authe.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category="error")
        elif len(email)<4:
            flash("PLease check your email,Email must be greater than 4 charecters.",category="error")
        elif len(firstName)<2:
            flash("firstName must be greater than 2", category="error")
        elif len(lastName) < 2:
            flash("lastName must be greater than 2", category="error")
        elif len(password1) < 7:
            flash("password must be greater than 7", category="error")
        elif password1 != password2 :
            flash("password don\'t match", category="error")
        else:
            new = User(email=email, first_name=firstName, last_name=lastName, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new)
            db.session.commit()
            flash("Your account is created", category="success")
            login_user(new)
            return redirect(url_for("view.home"))
    return render_template("sign-in.html",user=current_user)
