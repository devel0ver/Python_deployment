from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import users
import re

from flask_bcrypt import Bcrypt
from flask_app.models.users import User
bcrypt = Bcrypt(app)


class Event:
    db = "PlanIt"
    def __init__(self, data):
        self.id = data["id"]

        self.country = data["country"]
        self.location = data["location"]
        self.date_trip = data["date_trip"]
        self.time = data["time"]
        self.comments = data["comments"]
        self.user_id = data["user_id"]

        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.user = {}


    @staticmethod
    def event_valid(data):
        is_valid = True
        if data["country"] == "<-- select country -->":
            flash("Please select a country")
            is_valid = False
        if len(data["location"]) < 2:
            flash("Location must contain at least 2 characters")
            is_valid = False
        if data["date_trip"] == "":
            flash("Please select the date of your planned trip")
            is_valid = False
        if data["time"] == "":
            flash("Please select the time of your trip")
            is_valid = False
        return is_valid

    #==============================
    #  Insert a Event
    #==============================
    @classmethod
    def add_events(cls, data):
        query = """
        INSERT INTO trips (country, location, date_trip, time, comments, user_id, created_at) VALUES (%(country)s, %(location)s, %(date_trip)s, %(time)s, %(comments)s, %(user_id)s, NOW());
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    

    #==============================
    #  Get All Events
    #==============================
    @classmethod 
    def get_all(cls, data):
        query = "SELECT * FROM trips WHERE user_id = %(user_id)s"
        result = connectToMySQL(cls.db).query_db(query, data)

        trip = []
        for row in result:
            trip.append(cls(row))
        return trip
    

    #==============================
    #  Get a Event 
    #==============================
    @classmethod
    def get_event_w_user(cls, data):
        query = """
        SELECT * FROM trips LEFT JOIN users ON trips.user_id = users.id Where trips.id = %(event_id)s;
        """
        result = connectToMySQL(cls.db).query_db(query, data)

        event = cls(result[0])

        user_data = {
            "id" : result[0]["users.id"],
            "first_name" : result[0]["first_name"],
            "last_name" : result[0]["last_name"],
            "user_name" : result[0]["user_name"],
            "email" : result[0]["email"],
            "password" : result[0]["password"],
            "created_at" : result[0]["users.created_at"],
            "updated_at" : result[0]["users.updated_at"]
        }
        event.user = User(user_data)
        print(event)
        return event


    #==============================
    #  Edit a Event 
    #==============================
    @classmethod
    def update_event(cls, data):
        query = """
        UPDATE trips SET country = %(country)s, location = %(location)s, date_trip = %(date_trip)s, time = %(time)s, comments = %(comments)s, updated_at = NOW() WHERE id = %(event_id)s;
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        return 

    #==============================
    #  Delete a Event 
    #==============================
    @classmethod
    def delete_event(cls, data):
        query = "DELETE FROM trips WHERE id = %(event_id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        return
        