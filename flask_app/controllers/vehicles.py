from crypt import methods

from flask import flash, redirect, render_template, request, session

from flask_app import app
from flask_app.models.user import User
from flask_app.models.blog import Blog
from flask_app.models.vehicle import Vehicle


@app.route('/new/vehicle/to_db', methods=["POST"])      
def cars():
    if 'user_id' not in session:
        return redirect("/")
    if not Vehicle.validate_vehicle(request.form):
        return redirect("/dashboard")
    data ={
        "type":request.form["type"],
        "safety":request.form["safety"],
        "year":request.form["year"],
        "description":request.form['description'],
        "user_id":session["user_id"],
        "created_at":request.form['created_at']
        "updated_at": request.form['updated_at']
    }
    Vehicle.vehicle_info(data)  
    return redirect("/dashboard")

@app.route("/new")
def new_v():
    return render_template("newv.html")

@app.route('/vehicle')
def vehicle():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("vehicles.html",user=User.get_by_id(data), news = Vehicle.get_all_vehicles())