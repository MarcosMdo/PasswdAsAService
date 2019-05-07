def parseUser(registration):
    json_data = {}
    
    json_data['name'] = registration[0].rstrip()
    json_data['uid'] = registration[2].rstrip()
    json_data['gid'] = registration[3].rstrip()
    json_data['comment'] = registration[4].rstrip()
    json_data['home'] = registration[5].rstrip()
    json_data['shell'] = registration[6].rstrip()

    return json_data

def parseGroup(registration):
    json_data = {}

    members = registration[3].split(',')
    members[-1] = members[-1].rstrip()

    json_data['name'] = registration[0].rstrip()
    json_data['gid'] = registration[2].rstrip()
    json_data['members'] = members

    return json_data
