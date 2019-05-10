import markdown
import os
from urllib import parse
from flask import Flask, request, jsonify, abort
from .helper import parseToJson
import sys
app = Flask(__name__)

# Set sort keys off to return JSON in expected order.
app.config['JSON_SORT_KEYS'] = False

# base route path. Displays README file.
@app.route("/", methods=['GET'])
def index():
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as file:
        content = file.read()

        return markdown.markdown(content)

# Get all users method. Returns list of JSON objects
@app.route("/users", methods=['GET'])
def getAllUsers():
    result = []

    with open(os.path.dirname(app.root_path) + '/etc/passwd', 'r') as users:
        content = users.readline()
        while content[0] == '#':
            content = users.readline()
        while content:
            registration = content.split(':')
            json_data = parseToJson.parseUser(registration) # helper function to parse JSON
            result.append(json_data)

            content = users.readline()

    return jsonify(result)

# Get users via query, where only exact matches are allowed
# currently works, but way too slow when querying. will need to store
# passwd and group data in local db and quick access.
@app.route("/users/query", methods=['GET'])
def getUsersByQuery():
    args = request.args
    result = []
    flag = True

    with open(os.path.dirname(app.root_path) + '/etc/passwd', 'r') as users:
        content = users.readline()
        while content[0] == '#':
            content = users.readline()
        while content:
            flag = True
            registration = content.split(':')
            json_data = parseToJson.parseUser(registration)

            for key, value in args.items():
                if str(json_data[key]) != str(value):
                    flag = False
            if flag:
                result.append(json_data)

            content = users.readline()

    return jsonify(result)


# Get a user with a specific UID.
@app.route("/users/<string:uid>", methods=['GET'])
def getUserByUid(uid):
    with open(os.path.dirname(app.root_path) + '/etc/passwd', 'r') as users:
        content = users.readline()
        while content[0] == '#':
            content = users.readline()
        while content:
            registration = content.split(':')
            user_uid = registration[2]

            # Check if the passed in uid matches with the current contents uid.
            # If it does, parse JSON and return the found content.
            if int(user_uid) == int(uid):
                json_data = parseToJson.parseUser(registration)
                return jsonify(json_data)

            content = users.readline()
    abort(404)

# Get the groups of a user with a specific UID.
@app.route("/users/<string:uid>/groups", methods=['GET'])
def getUserGroupsByUid(uid):
    username = None
    result = []

    with open(os.path.dirname(app.root_path) + '/etc/passwd', 'r') as users:
        content = users.readline()
        while content[0] == '#':
            content = users.readline()
        while content:
            registration = content.split(':')
            user_uid = registration[2]

            # Check if the passed in uid matches with the current contents uid.
            # If it does, store username information, and scan through the groups 
            # file for a matching group with the username.
            if int(user_uid) == int(uid):
                username = registration[0]
                break

            content = users.readline()

    if username is None:
        return jsonify([])

    with open(os.path.dirname(app.root_path) + '/etc/group', 'r') as groups:
        content = groups.readline()
        while content[0] == '#':
            content = groups.readline()
        while content:
            registration = content.split(':')
            
            # We need to temporarily store the members of the content to compare.
            # The last member in the list is appended with a newline symbol, so 
            # we must strip it off of the members name for proper comparison.
            members = registration[3].split(',')
            members[-1] = members[-1].rstrip()

            if username in members:
                json_data = parseToJson.parseGroup(registration)
                result.append(json_data)

            content = groups.readline()

        return jsonify(result)

# Return a list of all groups on the system, defined by /etc/group
@app.route("/groups", methods=['GET'])
def getAllGroups():
    result = []

    with open(os.path.dirname(app.root_path) + '/etc/group', 'r') as groups:
        content = groups.readline()
        while content[0] == '#':
            content = groups.readline()
        while content:
            registration = content.split(':')
            json_data = parseToJson.parseGroup(registration)
            result.append(json_data)

            content = groups.readline()

    return jsonify(result)

# Return a list of groups matching all of the specified query fields.
@app.route("/groups/query", methods=['GET'])
def getGroupsByQuery():
    # We used args = request.args in the /users/query API call. 
    # Because we allow multiples of the same key (in this case, members) we need to parse the query 
    # parameters differently. Here we use parse_qs to parse the query string provided from the request
    argdict = parse.parse_qs(request.query_string.decode('utf8'))
    result = []
    flag = True

    with open(os.path.dirname(app.root_path) + '/etc/group', 'r') as groups:
        content = groups.readline()
        while content[0] == '#':
            content = groups.readline()
        while content:
            # The flag boolean will be used to determine if the content is passable by all parameters.
            # Because there are multiple checks, we need to hold the flags boolean value for final appending.
            flag = True

            # holds all members passed in via parameter. The ONLY variable that holds multiple values.
            members = [] 

            registration = content.split(':')
            json_data = parseToJson.parseGroup(registration)
        
            for key, value in argdict.items():
                # urllib.parse_qs returns the parsed query string as a Multidict object.
                # Due to this implementation, we need to access the first indice.
                # We only worry about the first indice of the keys that are not members because out API only
                # accepts duplicates of member values.  
                if key  == 'member':
                    for j in value:
                        members.append(j)
                elif json_data[key][0] != value[0]:
                    flag = False
                
            # Iterate all appended members from the query string and compare to all members found in this 
            # content, or group found in the /etc/group file.
            for m in members:
                if m not in json_data['members']:
                    flag = False

            if flag:
                result.append(json_data)

            content = groups.readline()

    return jsonify(result)

# Return a single group with <gid>. Return 404 if <gid> is not found.
@app.route("/groups/<string:gid>", methods=['GET'])
def getGroupbyGid(gid):
    with open(os.path.dirname(app.root_path) + '/etc/group', 'r') as groups:
        content = groups.readline()
        while content[0] == '#':
            content = groups.readline()
        while content:
            registration = content.split(':')
            user_gid = registration[2]

            if int(user_gid) == int(gid):
                json_data = parseToJson.parseGroup(registration)
                
                return jsonify(json_data)

            content = groups.readline()

    abort(404)
