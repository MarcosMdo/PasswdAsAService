import markdown
import os
from urllib import parse
from flask import Flask, request, jsonify, abort
from .helper import parseToJson
import sys
app = Flask(__name__)

# Set sort off to return JSON in expected order.
app.config['JSON_SORT_KEYS'] = False

# base route path. Displays README file.
@app.route("/")
def index():
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as file:

        content = file.read()
        return markdown.markdown(content)

# Get all users method. Returns list of JSON objects
@app.route("/users", methods=['GET'])
def getAllUsers():
    result = []
    with open(os.path.dirname(app.root_path) + '/passwd', 'r') as users:
        content = users.readline()

        while content:
            registration = content.split(':')
            json_data = parseToJson.parseUser(registration)
            result.append(json_data)

            content = users.readline()

    return jsonify(result)

# Get users via query, where only exact matches are allowed
# currently works, but way too slow when querying. will need to store
# passwd and group data in local db and quick access.
@app.route("/users/query")
def getUsersByQuery():
    args = request.args
    parse.urlencode(args)
    result = []
    flag = True

    with open(os.path.dirname(app.root_path) + '/passwd', 'r') as users:
        content = users.readline()

        while content:
            flag = True
            registration = content.split(':')
            json_data = parseToJson.parseUser(registration)

            for key, value in args.items():
                if str(json_data[key]) != str(value):
                    flag = False
            if flag:
                print("appending data.", file=sys.stderr)
                result.append(json_data)

            content = users.readline()

    return jsonify(result)


# Get a user with a specific UID.
@app.route("/users/<string:uid>")
def getUserByUid(uid):
    with open(os.path.dirname(app.root_path) + '/passwd', 'r') as users:
        content = users.readline()

        while content:
            registration = content.split(':')

            user_uid = registration[2]

            if int(user_uid) == int(uid):
                json_data = parseToJson.parseUser(registration)
                return jsonify(json_data)

            content = users.readline()
    abort(404)

# Get the groups of a user with a specific UID.
@app.route("/users/<string:uid>/groups")
def getUserGroupsByUid(uid):
    username = None
    result = []
    with open(os.path.dirname(app.root_path) + '/passwd', 'r') as users:
        content = users.readline()

        while content:
            registration = content.split(':')

            user_uid = registration[2]

            if int(user_uid) == int(uid):
                # scan this user in the groups file for their username
                username = registration[0]
                break

            content = users.readline()

    if username is None:
        return jsonify({})

    with open(os.path.dirname(app.root_path) + '/group', 'r') as groups:
        content = groups.readline()

        while content:
            registration = content.split(':')

            members = group_info[3].split(',')
            members[-1] = members[-1].rstrip()

            if username in members:
                json_data = parseToJson.parseGroup(registration)
                result.append(json_data)

            content = groups.readline()

        return jsonify(result)

# Return a list of all groups on the system, defined by /etc/group
@app.route("/groups")
def getAllGroups():
    result = []
    with open(os.path.dirname(app.root_path) + '/group', 'r') as groups:
        content = groups.readline()

        while content:
            registration = content.split(':')

            json_data = parseToJson.parseGroup(registration)
            result.append(json_data)

        content = groups.readline()

    return jsonify(result)

# Return a list of groups matching all of the specified query fields.
@app.route("/group/query")
def getGroupsByQuery():
    args = request.args
    parse.urlencode(args)
    result = []
    flag = True

    with open(os.path.dirname(app.root_path) + '/group', 'r') as groups:
        content = groups.readline()

        while content:
            flag = True
            registration = content.split(':')
            json_data = parseToJson.parseGroup(registration)

            for key, value in args.items():
                if str(json_data[key]) != str(value):
                    flag = False
            if flag:
                print("appending data.", file=sys.stderr)
                result.append(json_data)

            content = users.readline()

    return jsonify(result)



# Return a single group with <gid>. Return 404 if <gid> is not found.
@app.route("/groups/<string:gid>")
def getGroupbyGid(gid):
    with open(os.path.dirname(app.root_path) + '/group', 'r') as groups:
        content = groups.readline()

        while content:
            registration = content.split(':')

            user_gid = registration[2]

            if int(user_gid) == int(gid):

                json_data = parseToJson.parseGroup(registration)
                return jsonify(json_data)

            content = groups.readline()

    abort(404)
