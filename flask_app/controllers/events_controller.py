from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.users import User
from flask_app.models.events import Event
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)




#==============================
#  Event page
#==============================
@app.route('/home_page/event')
def events():
    if "search" not in session:
        session["search"] = "NewYork"
    if "user_id" not in session:
        flash("Please login or register!")
        return redirect('/')
    data = {
        "user_id" : session["user_id"]
    }
    user = User.get_by_id(data)
    events = Event.get_all(data)
    user_friend = User.show_friends(data)
    print(events)
    return render_template("events.html", user = user, location = session["search"], events = events, user_friend = user_friend)


#==============================
#  Add a Event 
#==============================
@app.route("/home_page/event_new", methods = ["POST"])
def new_events():
    data = {
        "country" : request.form["country"],
        "location" : request.form["location"],
        "date_trip" : request.form["date_trip"],
        "time" : request.form["time"],
        "comments" : request.form["comments"],
        "user_id" : session["user_id"]
    }
    if not Event.event_valid(data):
        return redirect("/home_page/event")
    Event.add_events(data)
    return redirect("/home_page/event")

#==============================
#  Search on map 
#==============================
@app.route("/search_location", methods = ["POST"])
def search():
    session["search"] = request.form["search"]
    return redirect("/home_page/event")


#==============================
#  Show a Event 
#==============================
@app.route("/home_page/event/show/<int:event_id>")
def show_event(event_id):
    if "user_id" not in session:
        flash("Please login or register!")
        return redirect('/')
    data = {
        "event_id" : event_id
    }
    event = Event.get_event_w_user(data)
    print(event)
    return render_template("show_event.html", event = event)

#==============================
#  Edit a Event 
#==============================
@app.route("/home_page/event/edit/<int:event_id>")
def edit_event(event_id):
    if "search" not in session:
        session["search"] = "NewYork"
    if "user_id" not in session:
        flash("Please login or register!")
        return redirect('/')
    data = {
        "event_id" : event_id
    }
    event = Event.get_event_w_user(data)
    print(event.time.seconds)
    output = {}
    output["H"], rem = divmod(event.time.seconds, 3600)
    output["M"], output["S"] = divmod(rem, 60)
    output["H"] = "0"+str(output["H"])
    output["M"] = "0" + str(output["M"])
    time = output["H"] +":"+ output["M"]
    print(output)
    return render_template("edit_event.html", event = event, location = session["search"], time = time)

@app.route("/home_page/event/update/<int:event_id>", methods=["POST"])
def update_event(event_id):
    data = {
        "country" : request.form["country"],
        "location" : request.form["location"],
        "date_trip" : request.form["date_trip"],
        "time" : request.form["time"],
        "comments" : request.form["comments"],
        "event_id" : event_id
    }
    Event.update_event(data)
    return redirect("/home_page/event")

#==============================
#  Delete a Event 
#==============================
@app.route("/home_page/event/delete/<int:event_id>")
def delete_event(event_id):
    data = {
        "event_id" : event_id
    }
    Event.delete_event(data)
    return redirect("/home_page/event")

