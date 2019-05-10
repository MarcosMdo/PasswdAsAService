# Password as a Service

Password as a service challenge for company recruitment.
The goal is to expose the user and group information on a UNIX system and create a minimal HTTP service that responds with group and user information dependent on the request.

This was written in Python under the Flask library and is Dockerized for ease of deployment.

## Run

To use default paths for user and group information:  
```./initialize.sh ```

To run with configured files:  
``` ./initialize.sh $path_to_folder_containing_both_files ```  
Note: the files must still be named ```passwd``` and ```group```

## Usage

### Get /users

Return a list of all users on the system, as defined in the /etc/passwd file.

```
[
  {
    “name”: “root”, “uid”: 0, “gid”: 0, “comment”: “root”, “home”: “/root”,
    “shell”: “/bin/bash”
  },
  {
    “name”: “dwoodlins”, “uid”: 1001, “gid”: 1001, “comment”: “”, “home”:
    “/home/dwoodlins”, “shell”: “/bin/false”
  }
]
```

### GET /users/query[?name=<nq>][&uid=<uq>][&gid=<gq>][&comment=<cq>][&home=<hq>][&shell=<sq]

Where Parameter list values are:
    * name
    * uid
    * gid
    * comment
    * home
    * shell

Only exact matches need to be supported.

Example Query:

GET /users/query?shell=%2Fbin%22Ffalse

Example Response:
```
[
  {
    "name": "dwoodlins", "uid": 1001, "gid":1001, "comment": "", "home": "/home/dwoodlins", "shell": "/bin/false"
  }
]
```
### GET /users/<uid>

Return a single user with <uid>. Return 404 if <uid> not found.

Example Response:
```
{
  “name”: “dwoodlins”, “uid”: 1001, “gid”: 1001, “comment”: “”, “home”: “/home/dwoodlins”, “shell”: “/bin/false”
}
```
### GET /users/<uid>/groups

Return all the groups for a given user.

Example Response:
```
[
  {
    “name”: “docker”, “gid”: 1002, “members”: [“dwoodlins”]
  }
]
```

### GET /groups

Return a list of all groups on the system, defined by /etc/group.

Example Response:
```
[
  {
    “name”: “_analyticsusers”, “gid”: 250, “members”: [“_analyticsd’,”_networkd”,”_timed”]
  },
  {
    “name”: “docker”, “gid”: 1002, “members”: []
  }
]
```
