from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from flask_app.models.vehicle import Vehicle
class Blog:
    db = "project_schema"
    def __init__(self,data):
        self.id = data['id']
        self.Post = data['Post']
        self.Location = data['Location']
        self.Rating = data['Rating']
        self.Date = data['Date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None


    @classmethod
    def blog_insert(cls,data):
        query = "INSERT INTO post (Post, Location, Rating, Date, user_id) VALUES(%(Post)s,%(Location)s,%(Rating)s,%(Date)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_all_blogs(cls):
        query = "SELECT * FROM post JOIN users ON post.user_id = users.id;"

        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        
        if len(results) == 0:              
            return[]
        else: 
            all_blogs = []
            for blog_dictionary in results:              
                blog_obj = cls(blog_dictionary)
                user_dictionary = {
                    "id" : blog_dictionary['users.id'],
                    "first_name" : blog_dictionary['first_name'],
                    "last_name" :blog_dictionary['last_name'],
                    "email" : blog_dictionary['email'],
                    "password" : blog_dictionary['password'],
                    "created_at" : blog_dictionary['users.created_at'],
                    "updated_at" : blog_dictionary['users.updated_at'],
                }

                user_obj = User(user_dictionary)

                blog_obj.user = user_obj

                all_blogs.append(blog_obj)
            return all_blogs
        


    @classmethod
    def get_one_blog(cls,data):
        query = "SELECT * FROM post JOIN users ON post.user_id = users.id WHERE post.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        
        if len(results) == 0:    
            return None
        else: 
            blog_dictionary = results[0]
            blog_obj = cls(results[0])
            user_dictionary = {
                "id" : blog_dictionary['users.id'],
                "first_name" : blog_dictionary['first_name'],
                "last_name" :blog_dictionary['last_name'],
                "email" : blog_dictionary['email'],
                "password" : blog_dictionary['password'],
                "created_at" : blog_dictionary['users.created_at'],
                "updated_at" : blog_dictionary['users.updated_at'],
            }

            user_obj = User(user_dictionary)

            blog_obj.user = user_obj
            return blog_obj
        
    @staticmethod
    def validate_blog(form_data):
        is_valid = True
        print(form_data)
        if len(form_data["Location"]) <= 0:
            flash("LOCATION CANNOT BE EMPTY!!!!")
            is_valid = False
        if len(form_data["Post"]) <= 0:
            flash("POST CANNOT BE EMPTY!!!!")
            is_valid = False
        if len(form_data["Rating"]) <= 0:
            flash("RATING CANNOT BE EMPTY!!!!")
            is_valid = False
        if len(form_data["Date"]) <= 0:
            flash("DATE CANNOT BE EMPTY!!!!")
            is_valid = False
        return is_valid
    
    @classmethod
    def delete_blog(cls, data):
        query = "DELETE FROM post WHERE id =%(id)s"
        return connectToMySQL(cls.db).query_db(query,data) 
    
    @classmethod
    def blog_edited(cls, data):
        query = "UPDATE post SET Post = %(Post)s, Rating = %(Rating)s, Location = %(Location)s, Date = %(Date)s WHERE id =%(id)s"
        return connectToMySQL(cls.db).query_db(query,data) 
        