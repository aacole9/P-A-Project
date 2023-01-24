from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models.user import User


class Vehicle:
    db = "project_schema"
    def __init__(self,data):
        self.id = data['id']
        self.type = data['type']
        self.safety = data['safety']
        self.description = data['description']
        self.year = data['year']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
    

    @classmethod
    def vehicle_info(cls,data):
        query = "INSERT INTO vehicles (type, safety, description, year, user_id) VALUES(%(type)s,%(safety)s,%(description)s,%(year)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data) 
    
    @classmethod
    def get_all_vehicles(cls):
        query = "SELECT * FROM vehicles JOIN users ON vehicles.user_id = users.id;"

        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        
        if len(results) == 0:    
            return[]
        else: 
            all_vehicles = []
            for vehicle_dictionary in results:    
                vehicle_obj = cls(vehicle_dictionary)
                user_dictionary = {
                    "id" : vehicle_dictionary['users.id'],
                    "first_name" : vehicle_dictionary['first_name'],
                    "last_name" : vehicle_dictionary['last_name'],
                    "email" : vehicle_dictionary['email'],
                    "password" : vehicle_dictionary['password'],
                    "created_at" : vehicle_dictionary['users.created_at'],
                    "updated_at" : vehicle_dictionary['users.updated_at'],

                }

                user_obj = User(user_dictionary)

                vehicle_obj.user = user_obj

                all_vehicles.append(vehicle_obj)
            return all_vehicles
        

    @classmethod
    def get_one_vehicle(cls,data):
        query = "SELECT * FROM vehicles JOIN users ON vehicles.user_id = users.id WHERE vehicles.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        
        if len(results) == 0:    
            return None
        else: 
            vehicle_dictionary = results[0]
            vehicle_obj = cls(results[0])
            user_dictionary = {
                "id" : vehicle_dictionary['users.id'],
                "first_name" : vehicle_dictionary['first_name'],
                "last_name" :vehicle_dictionary['last_name'],
                "email" : vehicle_dictionary['email'],
                "password" : vehicle_dictionary['password'],
                "created_at" : vehicle_dictionary['users.created_at'],
                "updated_at" : vehicle_dictionary['users.updated_at'],
            }

            user_obj = User(user_dictionary)

            vehicle_obj.user = user_obj
            return vehicle_obj
        
    @staticmethod
    def validate_vehicle(form_data):
        is_valid = True
        print(form_data)
        if len(form_data["year"]) <= 0:
            flash("YEAR CANNOT BE ZERO!!!!")
            is_valid = False
        if len(form_data["safety"]) <= 0:
            flash("SAFETY CANNOT BE EMPTY!!!!")
            is_valid = False
        if len(form_data["description"]) <= 0:
            flash("DESCRIPTION CANNOT BE EMPTY!!!!")
            is_valid = False
        if len(form_data["type"]) <= 0:
            flash("TYPE CANNOT BE EMPTY!!!!")
            is_valid = False
        return is_valid
    
    @classmethod
    def vehicle_edited(cls, data):
        query = "UPDATE vehicles SET type = %(type)s, safety = %(safety)s, year = %(year)s, description = %(description)s WHERE id =%(id)s"
        return connectToMySQL(cls.db).query_db(query,data) 
    
    @classmethod
    def delete_vehicle(cls, data):
        query = "DELETE FROM vehicles WHERE id =%(id)s"
        return connectToMySQL(cls.db).query_db(query,data) 