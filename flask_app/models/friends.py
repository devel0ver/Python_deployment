from unittest import result
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models.events import Events
from flask import flash


class Friend:
    db = "PlanIt"
    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.friend_id = data["friend_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]



    @classmethod
    def add_friend(cls, data):
        query = """
        INSERT INTO friends (user_id, friend_id, created_at)
        VALUES (%(user_id)s, %(friend_id)s, NOW());
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def remove_friends(cls, data):
        query = "DELETE FROM friends WHERE friend_id = %(friend_id)s and user_id = %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return

    