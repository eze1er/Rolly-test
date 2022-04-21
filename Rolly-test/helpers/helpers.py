from models.Answer import Answer
from models.Vote import Vote
from models.User import User


# get list of answers with coordinates of voters, vote count per answer
def answer_vote_count_coords(answers):
  return ([{
    'id': answer.id,
    'poll_id': answer.poll_id,
    'content': answer.content,
    'vote_count': Vote.query.filter(Vote.answer_id == answer.id).count(),
    'coordinates': [
        [
          user.latitude, user.longitude
        ]
        for user in User.query
          .with_entities(User.latitude, User.longitude)
          .join(Vote, User.id == Vote.user_id)
          .join(Answer, Vote.answer_id == Answer.id)
          .filter(Vote.answer_id == answer.id).all()
      ]
    }
    for answer in answers
])


# return poll, answers with vote count and voter coordinates, and user first & last name as dictionary
def poll_as_dict(poll):
  user = User.query.get(poll.user_id)

  poll_dict = poll.as_dict()
  poll_dict['first_name'] = user.first_name
  poll_dict['last_name'] = user.last_name
  poll_dict['answers'] = answer_vote_count_coords(poll.answers)

  return poll_dict
