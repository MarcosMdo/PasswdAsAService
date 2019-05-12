from password_service.views import configure_routes
from flask import Flask
import tempfile
import pytest
import urllib
import json
import sys
import os

app = Flask(__name__)
configure_routes(app)

def test_home_page(client):
  response = client.get('/')
  assert response.status_code == 200

def test_get_all_users(client):
  url = '/users'
  response = client.get(url)
  assert response.status_code == 200

def test_get_specific_user(client):
  total_users = 0
  with open(os.path.dirname(app.root_path) + '/tests/passwd', 'r') as users:
    content = users.readline()
    while content[0] == '#':
      content = users.readline()
    while content:
      user = content.split(':')
      response = client.get('/users/' + str(user[2]))
      data = json.loads(response.data)
      if data['uid'] == user[2]:
        total_users += 1
      content = users.readline()
  assert total_users == 14

def test_get_all_groups(client):
  url = '/groups'
  response = client.get(url)
  assert response.status_code == 200

def test_get_specific_group(client):
  total_groups = 0
  with open(os.path.dirname(app.root_path) + '/tests/group', 'r') as groups:
    content = groups.readline()
    while content[0] == '#':
      content = groups.readline()
    while content:
      group = content.split(':')
      response = client.get('/groups/' + str(group[2]))
      data = json.loads(response.data)
      if data['gid'] == group[2]:
        total_groups += 1
      content = groups.readline()
  assert total_groups == 42

def test_get_group_query(client):
  query_string = '?member=username'
  response = client.get(str('/groups/query' + query_string))
  data = json.loads(response.data)
  assert data[1]['name'] == 'dialout'

def test_get_user_query(client):
  query_string = "?shell=" + urllib.parse.quote('/usr/bin/ksh', safe='')
  response = client.get('/users/query' + query_string)
  data = json.loads(response.data)
  assert data[2]['name'] == 'paul'

def test_get_groups_from_user(client):
  response = client.get('/users/4/groups')
  data = json.loads(response.data)
  assert data[2]['name'] == 'syslog'

@pytest.fixture
def client():
  client = app.test_client()
  return client