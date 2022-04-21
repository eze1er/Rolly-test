from models.User import User
from models.VoterList import VoterList
from models.VoterListMember import VoterListMember
from models.VoterListPoll import VoterListPoll
from models.Poll import Poll
from helpers.helpers import poll_as_dict
from flask import request, jsonify, make_response
from database import db
from datetime import datetime
import json


# get all users
def index():
  return jsonify(User.query.all())


def get_user_by_email(user_id):
  user = User.query.get(user_id)

  # create user if user not exist
  if not user:
    user = User(user_id)
    db.session.add(user)
    db.session.commit()

  return jsonify(user)


def create_user():
  user_id = request.json['email']

  # return if user already exist
  if User.query.get(user_id):
    return make_response('User already exists', 400)

  user = User(user_id)

  db.session.add(user)
  db.session.commit()

  return jsonify(user)


def get_user_poll(user_id):
  q = Poll.query.filter(Poll.user_id == user_id)

  if request.args.get('time') == 'current':
    q = q.filter(Poll.user_id == user_id, Poll.end_at >= datetime.now())

  if request.args.get('time') == 'past':
    q = q.filter(Poll.user_id == user_id, Poll.end_at < datetime.now())

  return jsonify([poll_as_dict(poll) for poll in q.all()])


def get_user_invites(user_id):
  polls = (
    Poll.query
      .join(VoterListPoll, Poll.id == VoterListPoll.poll_id)
      .join(VoterList, VoterListPoll.voter_list_id == VoterList.id)
      .join(VoterListMember, VoterList.id == VoterListMember.voter_list_id)
      .filter(VoterListMember.user_id == user_id)
      .all()
  )

  return jsonify([poll_as_dict(poll) for poll in polls])


def get_user_voter_list(user_id):
  return jsonify({
    VoterList.id: [
      VoterListMember.user_id
      for VoterListMember in VoterList.voter_list_members
    ]
    for VoterList in VoterList.query
      .filter(VoterList.user_id == user_id)
      .all()
  })


def update_user():
  req = request.json
  user = User.query.get(req['id'])

  for key, val in req.items():
    setattr(user, key, val)

  db.session.commit()

  return jsonify(user)
