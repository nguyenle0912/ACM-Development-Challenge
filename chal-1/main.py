"""
Author: Nguyen Le
ACM Development Challenge

Challenge 1: 
For this challenge, you will build a simple service that allows a user to create "tags."
"""

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
api = Api(app)
app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #database to store tags
db = SQLAlchemy(app)


#Tag Model that can be stored in database
class TagModel(db.Model):
    tag_name = db.Column(db.String(100), primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    contents = db.Column(db.String(50000), nullable = False)
    token = db.Column(db.String(15), nullable = False)

    def __repr__(self): #string representation of this model
        return f"Tag(name = {name}, contents = {contents})"

db.create_all()


tag_post_args = reqparse.RequestParser() #automatically parse through requests that are being sent to make it fits the guidelines that are detailed in the following code
tag_post_args.add_argument("name", type=str, help="Name of Tag is required!") #to make arugment optional, set required = False
tag_post_args.add_argument("contents", type=str, help="Content of Tag is required")
tag_post_args.add_argument("token", type=str, help="Unique token for data retrieval")

tag_update_delete_args = reqparse.RequestParser() #parse arguments for update, each argument is optional
tag_update_delete_args.add_argument("name", type=str, help="Name of tag")
tag_update_delete_args.add_argument("contents", type=str, help="Contents of tag")
tag_update_delete_args.add_argument("token", type=str, help="Unique token for data retrieval")

#serialize Model to get a json response from model
post_resource_fields = {
    'name': fields.String,
    'contents': fields.String,
    'token': fields.String,
}

resource_fields = {
    'name': fields.String,
    'contents': fields.String,
}

def get_tag_with_keys(dict, get_keys): #this function allows get to only return name and contents and not token. 
    return {k:dict[k] for k in get_keys if k in dict}

class Tag(Resource):

    @marshal_with(post_resource_fields)
    def post(self, tag_name):
        args = tag_post_args.parse_args()
        result = TagModel.query.filter_by(name=tag_name).first() #check if video already exists
        if result:
            abort(409, message="Tag already exists") #abort if it already exists
        tag = TagModel(tag_name = tag_name, name = args['name'], contents = args['contents'], token = secrets.token_urlsafe(15))
        db.session.add(tag)
        db.session.commit()
        return tag, 201 #sucess post 

    @marshal_with(resource_fields)
    def get(self, tag_name):
        result = TagModel.query.filter_by(tag_name=tag_name).first()
        if not result:
            abort(404, message="Could not find tag with that name ...")
        return result
class Tag_Token(Resource):

    @marshal_with(resource_fields)
    def patch(self, tag_name, token): #update
        args = tag_update_delete_args.parse_args()
        result = TagModel.query.filter_by(tag_name = tag_name, token = token).first()
        if not result:
            abort(404, message="Video doesn't exist, cannot update...")
        
        if args['name']:
            result.name = args['name']
        if args['contents']:
            result.contents = args['contents']
        
        db.session.commit()
        return result

    def delete(self, tag_name, token):
        # if tags[tag_name]['token'] == token: #only tag with the given token will be deleted
        #     del tags[tag_name]
        #     return '200 OK'
        # else:
        return '404 Delete Failed', 404

api.add_resource(Tag, "/tags/<string:tag_name>") #for get and post requests
api.add_resource(Tag_Token, "/tags/<string:tag_name>/<string:token>") #for delete and patch requests

if __name__ == "__main__":
    app.run(debug=True)
