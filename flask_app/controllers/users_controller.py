from crypt import methods
from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.users import User
from flask_bcrypt import Bcrypt
from flask_app.models.friends import Friend
bcrypt = Bcrypt(app)

#==============================
#  The login page
#==============================
@app.route('/')
def login():
    return render_template('index.html')

@app.route('/login', methods=["POST"])
def logged():
    data ={
        "email" : request.form["email"],
        "password" : request.form["password"]
    }
    if not User.login_validate(data):
        return redirect("/")

    logged_in = User.get_by_email(data)
    session["user_id"] = logged_in.id

    return redirect('/home_page')

#==============================
#  The home page
#==============================
@app.route('/home_page')
def home():
    if "search_results" not in session:
        session["search_results"] = []
    if "user_id" not in session:
        flash("Please login or register!")
        return redirect('/')
    data = {
        "user_id" : session["user_id"]
    }
    user = User.show_friends(data)
    other_users = User.get_all_users(data)
    following = User.following(data)
    followers = User.followers(data)
    return render_template("home.html", user = user, other_users = other_users, search_results = session["search_results"], following = following, followers = followers)

#==============================
#  Followers
#==============================
@app.route('/home_page/<int:user_id>/followers')
def followers(user_id):
    return render_template("followers.html")
#==============================
#  Search Friends
#==============================
@app.route("/home_page/friend_search", methods=["POST"])
def friend_search():
    print(User.search_friend(request.form))
    session["search_results"] = User.search_friend(request.form)
    return redirect("/home_page")

#==============================
#  Profile
#==============================
@app.route("/home_page/profile")
def profile():
    if "user_id" not in session:
        flash("Please login or register!")
        return redirect('/')
    data = {
        "user_id" : session["user_id"]
    }
    user = User.get_by_id(data)
    return render_template("profile.html", user = user)

#==============================
#  Edit Profile
#==============================
@app.route("/home_page/profile/edit")
def edit_profile():
    if "user_id" not in session:
        flash("Please login or register!")
        return redirect('/')
    data = {
        "user_id" : session["user_id"]
    }
    user = User.get_by_id(data)
    return render_template("edit_profile.html", user=user)

@app.route("/home_page/profile/update", methods=["POST"])
def update_profile():
    data = {
        "user_id" : session["user_id"],
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "user_name" : request.form["user_name"],
        "email" : request.form["email"],
        "old_password" : request.form["old_password"],
        "password" : request.form["password"]
    }
    if not User.user_validate(data):
        return redirect("/home_page/profile/edit")
    return redirect("/home_page/profile")

#==============================
#  Delete Profile
#==============================
@app.route("/home_page/profile/delete/<int:user_id>")
def delete_profile(user_id):
    if "user_id" not in session:
        flash("Please login or register!")
        return redirect('/')
    data = {
        "user_id" : session["user_id"]
    }
    user = User.get_by_id(data)
    return render_template("delete_account.html", user = user)

@app.route("/home_page/profile/delete/<int:user_id>/success")
def deleted_profile(user_id):
    data = {
        "user_id" : user_id
    }
    User.delete_friends_w_user(data)
    User.delete_events_w_user(data)
    User.delete_user(data)
    session.clear()
    return redirect("/")


#==============================
#  The register page
#==============================
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/new_account', methods=["POST"])
def new_account():
    
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "user_name" : request.form["user_name"],
        "password" : request.form["password"],
        "conf_pass" : request.form["conf_pass"]
    }
    if not User.user_validate(data):
        return redirect("/register")

    pw_hash = bcrypt.generate_password_hash(request.form["password"])

    # update the password field of our data object to be the hashed password
    data["password"] = pw_hash
    user = User.add_user(data)
    session["user_id"] = user
    print(session["user_id"])
    return redirect('/')

#==============================
#  The about page
#==============================
@app.route('/about')
def about():
    return render_template('about.html')

#==============================
#  Logout page
#==============================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')