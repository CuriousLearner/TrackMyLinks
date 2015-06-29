from src import app, db
from flask import (render_template, jsonify, request, redirect, url_for, 
                   Response, make_response)
from models import Resource, Tags
import json

result = [] # Global result list to return result as JSON
r = Resource() # Global Instance of Resource

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/resource/addresources/', methods=['GET', 'POST'])
def add_resource():
    '''
    adds resources with POST request
    '''
    if request.method == 'POST':
        if request.json:
            global r
            r = Resource()
            # r.rid = request.json['rid'] # Now automatically updated
            r.title = request.json['title']
            r.link = str(request.json['link'])
            # Insert Tags to Tags Object
            r.tags = []
            for item in request.json['tags']:
                t = Tags()
                t.tag_name = item['tag_name']
                r.tags.append(t)
            r.description = request.json['description']
            r.save()
    return Response(json.dumps(r, cls=PythonJSONEncoder), status=200, 
                    content_type="application/json")

@app.route('/api/resource/getresources/')
def get_resources():
    '''
    returns all the resources with GET request
    '''
    global result
    allResources = Resource.objects.all()
    create_dict(allResources)
    return Response(json.dumps(result, cls=PythonJSONEncoder), status=200, 
                    content_type="application/json")

@app.route('/api/resource/getresources/<int:resource_id>/')
def update_or_delete_resource(resource_id):
    '''
    Depending on the request,
    GET: Get the given resource
    PUT: Update the resource 
    or DELETE: Delete the resource
    '''
    global result
    allResources = Resource.objects.filter(rid=resource_id)
    if allResources: # Resource is available in DB
        if request.method == 'PUT': # Update the resource
            pass
        if request.method == 'DELETE': # Delete the resource
            pass
        create_dict(allResources)
    else:
        result = [{'Error': 'Resource not found'}]
    return Response(json.dumps(result, cls=PythonJSONEncoder), status=200, 
                    content_type="application/json")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Not found'}), 404)


class PythonJSONEncoder(json.JSONEncoder):
    """
    Custom JSON Encoder to encode unsupported data-types to pythonic
    representations.
    """
    def default(self, obj):
        if isinstance(obj, Resource):
            return obj.get_dict()
        elif isinstance(obj, Tags):
            return obj.get_dict()
        else:
        	return repr(obj)
        return super(PythonJSONEncoder, self).default(obj)

def unjsonify(dct):
    if 'rid' in dct:
        dct['rid']=round(eval(dct['rid']), 1)
    return dct

def create_dict(allResources):
    global result # To store the result of all resources
    result = [] # Empty for each call
    for item in allResources:
        d = {} # To make a dictionary for JSON Response
        d['rid'] = item.rid
        d['title'] = item.title
        d['link'] = item.link
        d['tags'] = item.tags
        d['description'] = item.description
        result.append(d)
    return result