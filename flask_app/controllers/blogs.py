from crypt import methods

from flask import flash, redirect, render_template, request, session

from flask_app import app
from flask_app.models.user import User
from flask_app.models.blog import Blog
from flask_app.models.vehicle import Vehicle


# Route that will show the blog posts


# Route that will let you make a blog post to the new_blogs page
@app.route("/post")
def post_blog():
    return render_template("post.html")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html", user=User.get_by_id(data))

@app.route('/blogs')
def blogs():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("blog.html",user=User.get_by_id(data), new_system = Blog.get_all_blogs())


@app.route('/blogs/to_db', methods=["POST"])      
def blog():
    if 'user_id' not in session:
        return redirect("/")
    if not Blog.validate_blog(request.form):
        return redirect("/post")
    data ={
        "Location":request.form["Location"],
        "Rating":request.form["Rating"],
        "Post":request.form["Post"],
        "Date":request.form["Date"],
        "user_id":session["user_id"]
    }
    Blog.blog_insert(data)  
    return redirect("/blogs")  

@app.route('/vote')
def voting():
    return render_template("vote.html")


@app.route("/new")
def new_v():
    return render_template("newv.html")

@app.route('/new/vehicle/to_db', methods=["POST"])      
def vehicle_db():
    if 'user_id' not in session:
        return redirect("/")
    if not Vehicle.validate_vehicle(request.form):
        return redirect("/new")
    data ={
        "type":request.form["type"],
        "safety":request.form["safety"],
        "year":request.form["year"],
        "description":request.form['description'],
        "user_id":session["user_id"],
    }
    Vehicle.vehicle_info(data)  
    return redirect("/vehicles")

@app.route('/vehicles')
def vehicles():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("vehicles.html",user=User.get_by_id(data), new_system = Vehicle.get_all_vehicles())

@app.route("/edit/<int:id>/new_db", methods=["POST"])      
def vehicle_edited(id):
    if 'user_id' not in session:
        return redirect("/")    
    if not Vehicle.validate_vehicle(request.form):
        return redirect("/vehicles")
    data ={
        "type":request.form["type"],
        "safety":request.form["safety"],
        "year":request.form["year"],
        "description":request.form['description'],
        "id": id
    }
    Vehicle.vehicle_edited(data)  
    return redirect("/vehicles")

@app.route("/delete/<int:id>")
def delete_vehicle(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id" : id
    }
    Vehicle.delete_vehicle(data)
    return redirect("/dashboard")

@app.route("/edit/<int:id>")
def edit_vehicle(id):
    if 'user_id' not in session:
        return redirect("/")
    data = {
        "id" : id,  
    }
    return render_template("edit.html", user=User.get_by_id(data), newer = Vehicle.get_one_vehicle(data))

@app.route("/blog/delete/<int:id>")
def delete_blog(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id" : id
    }
    Blog.delete_blog(data)
    return redirect("/blogs")

@app.route("/blogs/edit/<int:id>/new_db", methods=["POST"])      
def blog_edited(id):
    if 'user_id' not in session:
        return redirect("/")    
    if not Blog.validate_blog(request.form):
        return redirect("/post")
    data ={
        "Post":request.form["Post"],
        "Location":request.form["Location"],
        "Rating":request.form["Rating"],
        "Date":request.form['Date'],
        "id": id
    }
    Blog.blog_edited(data)  
    return redirect("/blogs")

@app.route("/blogs/edit/<int:id>")
def edit_blog(id):
    if 'user_id' not in session:
        return redirect("/")
    data = {
        "id" : id,  
    }
    datas = {
        "id": session['user_id']
    }
    return render_template("edit_blog.html", user=User.get_by_id(datas), newer = Blog.get_one_blog(data))