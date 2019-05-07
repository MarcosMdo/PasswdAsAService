def parseUser(registration):
    json_data = {}

    json_data['name'] = registration[0]
    json_data['uid'] = registration[2]
    json_data['gid'] = registration[3]
    json_data['comment'] = registration[4]
    json_data['home'] = registration[5]
    json_data['shell'] = registration[6]

    return json_data

def parseGroup(registration):
    json_data = {}

    members = registration[3].split(',')
    members[-1] = members[-1].rstrip()

    json_data['name'] = registration[0]
    json_data['gid'] = registration[2]
    json_data['members'] = members

    return json_data
