from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "placement_secret"

#DATABASE CONFIG

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:131315@localhost:3306/placement_tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#MODELS

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Company(db.Model):
    __tablename__ = "companies"

    company_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    package_lpa = db.Column(db.Float, nullable=False)
    drive_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), default="Applied")

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    user = db.relationship("User", backref="companies")

#Home

@app.route("/")
def home():
    return render_template("index.html")

#Register

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]

        existing_user=User.query.filter_by(email=email).first()
        if existing_user:
            flash("email already exist")
            return redirect(url_for("login"))
        new_user=User(
            full_name=name,email=email,password=password
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration Successfull please login")
        return redirect(url_for("login"))
    return render_template("register.html")

#Login

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]

        user=User.query.filter_by(
            email=email,
            password=password
        ).first()
        if user:
            session["user_id"]=user.user_id
            session["user_name"]=user.full_name
            flash("login successfull")
            return redirect(url_for("dashboard"))
        else:
            flash("invalid password or email")

    return render_template("login.html")

#Dash Board

@app.route("/dashboard",methods=["GET","POST"])
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    companies=Company.query.filter_by(
        user_id=session["user_id"]
    ).all()

    total_companies=len(companies)

    return render_template("dashboard.html",
                           companies=companies,
                           total_companies=total_companies
                           )

#add-company

@app.route("/add-company",methods=["GET","POST"])
def add_company():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method=="POST":

        drive_date = datetime.strptime(
            request.form["drive_date"],
            "%Y-%m-%d"
        ).date()
          
        company=Company(
            company_name = request.form["company_name"],
            role = request.form["role"],
            package_lpa = request.form["package_lpa"],
            drive_date = drive_date,
            status = request.form["status"],
            user_id=session["user_id"]

        )
    
        db.session.add(company)
        db.session.commit()
        flash("company added successfully ")
        return redirect(url_for("dashboard"))
    return render_template("add-company.html")
#LOGOUT

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged Out Successfully")

    return redirect(url_for("home"))


#MAIN

if __name__ == "__main__":
    app.run(debug=True)