from models.Vote import Vote
from models.User import User
from models.Poll import Poll
from models.VoterList import VoterList
from models.VoterListPoll import VoterListPoll
from models.VoterListMember import VoterListMember
from models.Answer import Answer
from flask import request, jsonify, make_response
from database import db
from datetime import datetime
from geopy.distance import geodesic



def index():
  if request.method == 'GET':
    # return all votes
    return jsonify(Vote.query.all())

  req = request.json

  # validate poll
  poll = Poll.query.get(req['poll_id'])
  if not poll:
    return make_response('Invalid poll_id', 400)

  # validate answer
  answer = Answer.query.get(req['answer_id'])
  if not answer or answer.poll_id != poll.id:
    return make_response('Invalid answer_id', 400)

  vote = Vote.query.filter_by(user_id=req['user_id'], poll_id=poll.id)

  if request.method == 'POST':
    user = User.query.get(req['user_id'])
    # check voter list
    if poll.restriction:
      q = (
        VoterListMember.query
          .join(VoterList, VoterListMember.voter_list_id == VoterList.id)
          .join(VoterListPoll, VoterList.id == VoterListPoll.voter_list_id)
          .filter(VoterListPoll.poll_id == poll.id, VoterListMember.user_id == user.id)
          .all()
      )
      if not q:
        return make_response('User not authorized to vote in this poll', 403)

    # check location
    # if geodesic((user.latitude, user.longitude), (poll.latitude, poll.longitude)).km > poll.radius:
    #   return('Cannot vote in this location', 403)

    # create vote if user has not voted
    vote = vote.first()
    if not vote:
      vote = Vote(user.id, poll.id, req['answer_id'])
      db.session.add(vote)
      db.session.commit()
      return jsonify(vote)

    return make_response('Cannot vote twice', 403)

  # check if vote exists
  if not vote.first():
    return make_response('Vote does not exist', 400)

  # update vote
  if request.method == 'PUT':
    vote = vote.first()
    for key, val in req.items():
      setattr(vote, key, val)

    db.session.commit()
    return jsonify(vote)

  # delete vote
  vote.delete()
  db.session.commit()

  return make_response('Success', 200)
