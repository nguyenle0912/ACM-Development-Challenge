"""
Author: Nguyen Le
ACM Development Challenge

Challenge 1: 
For this challenge, you will build a simple service that allows a user to create "tags."
"""

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
import secrets

app = Flask(__name__)
api = Api(app)

tag_post_args = reqparse.RequestParser() #automatically parse through requests that are being sent to make it fits the guidelines that are detailed in the following code
tag_post_args.add_argument("name", type=str, help="Name of Tag is required!") #to make arugment optional, set required = False
tag_post_args.add_argument("contents", type=str, help="Content of Tag is required")
tag_post_args.add_argument("token", type=str, help="Unique token for data retrieval")

tags = {} #storage

def abort_if_tag_doesnt_exist(tag_name):
    if tag_name not in tags:
        print("aborting..")
        abort(404, message="Could not find tag " + tag_name)

def abort_if_tag_exists(tag_name):
    if tag_name in tags:
        abort(409, message="Tag already exists with that name")

def get_tag_with_keys(dict, get_keys): #this function allows get to only return name and contents and not token. 
    return {k:dict[k] for k in get_keys if k in dict}

class Tag(Resource):
    def post(self, tag_name):
        abort_if_tag_exists(tag_name)
        args = tag_post_args.parse_args()
        tags[tag_name] = args
        tags[tag_name]['token'] = secrets.token_urlsafe(15) #add unique token for every new post
        return tags[tag_name], 201 #sucess post 

    def get(self, tag_name):
        abort_if_tag_doesnt_exist(tag_name)
        get_keys = ['name', 'contents']
        tag = get_tag_with_keys(tags[tag_name], get_keys)
        return tag #success 200

class Tag_Token(Resource):
    def patch(self, tag_name, token):
        abort_if_tag_doesnt_exist(tag_name)
        if tags[tag_name]['token'] == token:
            args = tag_post_args.parse_args()
            tags[tag_name] = args
            return tags[tag_name]

    def delete(self, tag_name, token):
        abort_if_tag_doesnt_exist(tag_name)
        if tags[tag_name]['token'] == token: #only tag with the given token will be deleted
            del tags[tag_name]
            return '200 OK'
        else:
            return '404 Delete Failed', 404

api.add_resource(Tag, "/tags/<string:tag_name>") #for get and post requests
api.add_resource(Tag_Token, "/tags/<string:tag_name>/<string:token>") #for delete and patch requests

if __name__ == "__main__":
    app.run(debug=True)
