from crypt import methods
from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.users import User
from flask_app.models.friends import Friend


#==============================
#  Add Friends
#==============================
@app.route("/addfriend/<int:user_id>/<int:friend_id>")
def add_friend(user_id, friend_id):
    data = {
        "user_id" : user_id,
        "friend_id" : friend_id
    }
    con = True
    friends = User.show_friends(data)
    for user in friends.friends:
        print(user.id, friend_id)
        if friend_id == user.id:
            flash("User is already your friend!")
            con = False
            break
    if con:
        User.add_friend(data)
    return redirect("/home_page")


#==============================
#  Remove Friends
#==============================
@app.route("/remove_friend/<int:user_id>/<int:friend_id>")
def remove_friend(user_id, friend_id):
    data = {
        "user_id" : user_id,
        "friend_id" : friend_id
    }
    Friend.remove_friends(data)
    return redirect("/home_page")