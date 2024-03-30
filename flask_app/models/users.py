from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models.events import Events
from flask_app.models import friends
from flask import flash
import re

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db = "PlanIt"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.user_name = data["user_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.friends = []




    @staticmethod
    def user_validate(data):
        is_valid = True
        if len(data["first_name"]) < 3 and len(data["last_name"]) < 3:
            flash("Name must have at least 3 characters")
            is_valid = False
        if User.get_by_user_name(data):
            flash("User name is already in use!")
            is_valid = False
        if len(data['user_name']) < 4:
            flash("User name must contain at least 4 characters")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email")
            is_valid = False
        if User.get_by_email(data):
            flash("Email is already use! Please use another email.")
            is_valid = False
        if len(data["password"]) < 6:
            flash("Password must contain at least 8 characters")
            is_valid = False
        if data["password"] != data["conf_pass"]:
            flash("Password must match!")
            is_valid = False
        return is_valid

    @staticmethod
    def login_validate(data):
        is_valid = True
        user_in_db = User.get_by_email(data)
        if not user_in_db:
            flash("Invalid Credentials!")
            is_valid = False
        elif not bcrypt.check_password_hash(user_in_db.password, data['password']):
            flash("Invalid Credentials!")
            is_valid = False
        return is_valid


    #=====================================
    #   Add User
    #=====================================
    @classmethod
    def add_user(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, user_name, email, password, created_at)
        VALUES (%(first_name)s, %(last_name)s, %(user_name)s, %(email)s, %(password)s, NOW());
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    #=====================================
    #   Get by Email
    #=====================================
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])
    #=====================================
    #   Get by Password
    #=====================================
    # @classmethod
    # def get_by_password(cls,data):
    #     query = "SELECT * FROM users WHERE password = %(old_password)s;"
    #     result = connectToMySQL(cls.db).query_db(query,data)
    #     # Didn't find a matching user
    #     if len(result) < 1:
    #         return False
    #     return cls(result[0])

    #=====================================
    #   Get by User name
    #=====================================
    @classmethod
    def get_by_user_name(cls,data):
        query = "SELECT * FROM users WHERE user_name = %(user_name)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])
    
    #=====================================
    #   Get all users by id
    #=====================================
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    #=====================================
    #   Get all users
    #=====================================
    @classmethod
    def get_all_users(cls, data):
        query = "SELECT * FROM users WHERE id != %(user_id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    #=====================================
    #   Delete a users
    #=====================================
    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM users WHERE id = %(user_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return
    @classmethod
    def delete_friends_w_user(cls, data):
        query = "DELETE FROM friends WHERE user_id = %(user_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return
    @classmethod
    def delete_events_w_user(cls, data):
        query = "DELETE FROM trips WHERE user_id = %(user_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return

    #=====================================
    #   Search for friends LIKE(%)
    #=====================================
    @classmethod
    def search_friend(cls, data):
        new_data = {"user_name" : data['user_name'] + "%%"}
        print(new_data)
        query = "SELECT * FROM users WHERE user_name LIKE %(user_name)s;"
        result = connectToMySQL(cls.db).query_db(query, new_data)
        return result

    #=====================================
    #   Add a friend
    #=====================================
    @classmethod
    def add_friend(cls, data):
        query = """
        INSERT INTO friends (user_id, friend_id, created_at)
        VALUES (%(user_id)s, %(friend_id)s, NOW());
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    #=====================================
    #   Show friends
    #=====================================
    @classmethod
    def show_friends(cls, data):
        query = """
        SELECT * FROM users
        LEFT JOIN friends ON users.id = friends.user_id
        LEFT JOIN users as friend ON friend.id = friends.friend_id
        WHERE users.id = %(user_id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        user = cls(results[0])
        for row in results:
            friend_data = {
                "id" : row["friend.id"],
                "first_name" : row["friend.first_name"],
                "last_name" : row["friend.last_name"],
                "user_name" : row["friend.user_name"],
                "email" : row["friend.email"],
                "password" : row["friend.password"],
                "created_at" : row["friend.created_at"],
                "updated_at" : row["friend.updated_at"]
            }
            user.friends.append(cls(friend_data))
        print(user)
        return user

    #=====================================
    #   count following
    #=====================================
    @classmethod
    def following(cls, data):
        query = """
        SELECT COUNT(friends.friend_id) as following FROM users
        LEFT JOIN friends ON users.id = friends.user_id
        LEFT JOIN users as friend ON friend.id = friends.friend_id
        WHERE users.id = %(user_id)s
        GROUP BY users.id;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        return results
    #=====================================
    #   count followers
    #=====================================
    @classmethod
    def followers(cls, data):
        query = """
        SELECT COUNT(friends.user_id) as followers FROM users
        LEFT JOIN friends ON users.id = friends.user_id
        LEFT JOIN users as friend ON friend.id = friends.friend_id
        WHERE friends.friend_id = %(user_id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        return results