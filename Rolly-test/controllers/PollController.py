from models.Poll import Poll
from models.Answer import Answer
from models.VoterListPoll import VoterListPoll
from models.Vote import Vote
from helpers.helpers import poll_as_dict
from flask import request, jsonify
from database import db
from datetime import datetime
from sqlalchemy import func


def create_poll():
  req = request.json

  # create poll
  poll = Poll(
    req['user_id'],
    req['category'],
    req['name'],
    req['region'],
    True if req['emailList'] else False,
    req['description'],
    req['start_at'],
    req['end_at'],
    req['center'][1],
    req['center'][0],
    req['radius'],
    req['visibility']
  )

  db.session.add(poll)
  db.session.flush()

  # create answers
  for item in req['answers']:
    answer = Answer(poll.id, item)
    db.session.add(answer)

  # create email list
  if req['emailList']:
    for item in req['emailList']:
      voter_list_poll = VoterListPoll(item, poll.id)
      db.session.add(voter_list_poll)

  db.session.commit()

  return jsonify(poll_as_dict(poll))


def get_poll_by_id(id):
  return jsonify(poll_as_dict(Poll.query.get(id)))


def filter_polls():
  # query polls without restriction
  q = Poll.query.filter(Poll.restriction == False)

  # filter by time
  if request.args.get('time'):
    if request.args['time'] == 'current':
      q = q.filter(Poll.end_at >= datetime.now(), Poll.start_at <= datetime.now())
    else:
      q = q.filter(Poll.end_at < datetime.now())

  # filter by region
  if request.args.get('region'):
    q = q.filter(Poll.region == request.args['region'])

  # filter by category
  if request.args.get('category'):
    q = q.filter(Poll.category == request.args['category'])

  if request.args.get('order'):

    # order by popularity
    if request.args['order'] == 'popularity':
      subquery = (
        db.session
          .query(Vote)
          .with_entities(Vote.poll_id, func.count().label('popularity'))
          .group_by(Vote.poll_id)
          .subquery()
      )
      q = (
        q.join(subquery, Poll.id == subquery.c.poll_id)
          .order_by(subquery.c.popularity.desc())
      )

    # order by newest
    elif request.args['order'] == 'new':
      q = q.order_by(Poll.created_at.desc())

    # order by oldest
    else:
      q = q.order_by(Poll.created_at.asc())

  # return the first 9 polls
  return jsonify([poll_as_dict(poll)for poll in q.limit(9).all()])


def update_poll():
  req = request.json
  poll = Poll.query.get(req['id'])

  for key, val in req.items():
    setattr(poll, key, val)

  db.session.commit()

  return jsonify(poll_as_dict(poll))
