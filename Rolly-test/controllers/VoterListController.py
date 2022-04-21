from models.VoterList import VoterList
from models.VoterListMember import VoterListMember
from flask import request, jsonify
from database import db


def index():
  return jsonify(VoterList.query.all())


def create_voter_list():
  req = request.json
  voter_list = VoterList(req['user_id'], req['name'])

  db.session.add(voter_list)
  db.session.flush()

  for email in req['emails']:
    voter_list_member = VoterListMember(voter_list.id, email)
    db.session.add(voter_list_member)

  db.session.commit()

  return jsonify(voter_list, voter_list.voter_list_members)
