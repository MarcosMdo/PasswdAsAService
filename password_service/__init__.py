import markdown
import os
from flask import Flask, request, jsonify, abort

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
    with open(os.path.dirname(app.root_path) + '/passwds', 'r') as users:
        content = users.readline()

        while content:
            registration = content.split(':')
            username = registration[0]
            uid = registration[2]
            gid = registration[3]
            comment = registration[4]
            home = registration[5]
            shell = registration[6]

            json_data = {}
            json_data['name'] = username
            json_data['uid'] = uid
            json_data['gid'] = gid
            json_data['comment'] = comment
            json_data['home'] = home
            json_data['shell'] = shell

            result.append(json_data)
            content = users.readline()

    return jsonify(result)

# Get a user with a specific UID.
@app.route("/users/<string:uid>")
def getUserByUid(uid):
    with open(os.path.dirname(app.root_path) + '/passwds', 'r') as users:
        content = users.readline()

        while content:
            registration = content.split(':')

            user_uid = registration[2]

            if int(user_uid) == int(uid):
                username = registration[0]
                gid = registration[3]
                comment = registration[4]
                home = registration[5]
                shell = registration[6]

                json_data = {}
                json_data['name'] = username
                json_data['uid'] = uid
                json_data['gid'] = gid
                json_data['comment'] = comment
                json_data['home'] = home
                json_data['shell'] = shell

                return jsonify(json_data)
            content = users.readline()
    abort(404)

# Get the groups of a user with a specific UID.
@app.route("/users/<string:uid>/groups")
def getUserGroupsByUid(uid):
    username = None
    result = []
    with open(os.path.dirname(app.root_path) + '/passwds', 'r') as users:
        content = users.readline()

        while content:
            registration = content.split(':')

            user_uid = registration[2]

            if int(user_uid) == int(uid):
                # scan this user in the groups file for their
                username = registration[0]
                break

            content = users.readline()
    with open(os.path.dirname(app.root_path) + '/group', 'r') as groups:
        content = groups.readline()

        while content:
            group_info = content.split(':')
            members = group_info[3].split(',')
            members[-1] = members[-1].rstrip()
            if username in members:
                group_name = group_info[0]
                gid = group_info[2]

                json_data = {}
                json_data['name'] = group_name
                json_data['gid'] = gid
                json_data['members'] = members

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
            group_name = registration[0]
            gid = registration[2]
            members = registration[3].split(',')
            members[-1] = members[-1].rstrip()

            json_data = {}
            json_data['name'] = group_name
            json_data['gid'] = gid
            json_data['members'] = members
            result.append(json_data)

        content = groups.readline()

    return jsonify(result)
