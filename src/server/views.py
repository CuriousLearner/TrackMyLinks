from server import app, db
from flask import (render_template, jsonify, request, redirect, url_for,
                   Response, make_response)
from models import Resource, Tags
from operator import itemgetter
import json

result = []  # Global result list to return result as JSON
r = Resource()  # Global Instance of Resource


@app.route('/api/resource/addresources/', methods=['GET', 'POST'])
def add_resource():
    '''
    adds resources with POST request
    '''
    if request.method == 'POST':
        request_json()
    return Response(json.dumps({"Message": "Resource Added Successfully"}, cls=PythonJSONEncoder), status=200,
                    content_type="application/json")


@app.route('/api/resource/getresources/')
def get_resources():
    '''
    returns all the resources with GET request
    :arg:resource_id: GET request with that resource id
    '''
    global result
    resource_id = request.args.get('resource_id')
    if resource_id:
        result = Resource.objects.get(rid=resource_id)
    else:
        allResources = Resource.objects.all()
        create_dict(allResources)
        result = sorted(result, key=itemgetter('rid'))
    return Response(json.dumps(result, cls=PythonJSONEncoder), status=200,
                    content_type="application/json")


@app.route('/api/resource/updateresources/<int:resource_id>/', methods=['PUT',
                                                                        'DELETE'])
def update_or_delete_resource(resource_id):
    '''
    Depending on the request,
    PUT: Update the resource 
    or DELETE: Delete the resource
    '''
    global result
    allResources = Resource.objects.get(rid=resource_id)
    if allResources:  # Resource is available in DB
        if request.method == 'PUT':  # Update the resource
            modified_json = create_dict_for_update(request.json)
            allResources.update(**modified_json)
            result = [{"Message": "Resource Updated Successfully"}]
        if request.method == 'DELETE':  # Delete the resource
            allResources.delete()
            result = [{"Message": "Resource Deleted Successfully"}]
    else:
        result = [{"Message": "Resource not found"}]
    return Response(json.dumps(result, cls=PythonJSONEncoder), status=200,
                    content_type="application/json")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"Error": "Not found"}), 404)


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
        dct['rid'] = round(eval(dct['rid']), 1)
    return dct


def create_dict(allResources):
    global result  # To store the result of all resources
    result = []  # Empty for each call
    for item in allResources:
        d = {}  # To make a dictionary for JSON Response
        d['rid'] = item.rid
        d['title'] = item.title
        d['link'] = item.link
        d['tags'] = item.tags
        d['description'] = item.description
        result.append(d)
    return result


def request_json(**kwargs):
    if request.json:
        global r
        r = Resource()
        for k, v in kwargs.iteritems():
            r.rid = v  # Now automatically updated
        r.title = request.json['title']
        r.link = str(request.json['link'])
        # Insert Tags to Tags Object
        r.tags = []
        for item in request.json['tags']:
            t = Tags()
            t.tag_name = item['tag_name']
            r.tags.append(t)
        r.description = request.json['description']
        r.save(upsert=True)


def create_dict_for_update(JSONDoc):
    for k, v in JSONDoc.iteritems():
        k = "set__" + str(k)
    return JSONDoc

##########################################################################
#                               For Pre-flight Requests
#           My app was working good with normal request like GET and POST,
#           but for pre-flight requests like PUT, DELETE, from front-end, CORS error
#           appeared. There was a need to reply to the OPTIONS first, before the actual
#           request and then stumbled upon this:
#           http://coalkids.github.io/flask-cors.html
#
##########################################################################


@app.before_request
def option_autoreply():
    """ Always reply 200 on OPTIONS request """

    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        h = resp.headers

        # Allow the origin which made the XHR
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        # Allow the actual method
        h['Access-Control-Allow-Methods'] = request.headers[
            'Access-Control-Request-Method']
        # Allow for 10 seconds
        h['Access-Control-Max-Age'] = "10"

        h['Content-Type'] = 'application/json'
        print("type of request" + str(type(h['Access-Control-Allow-Origin'])))
        # We also keep current headers
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers

        return resp


@app.after_request
def set_allow_origin(resp):
    """ Set origin for GET, POST, PUT, DELETE requests """

    h = resp.headers

    # Allow crossdomain for other HTTP Verbs
    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        h['Access-Control-Allow-Origin'] = request.headers['Origin']

    return resp
