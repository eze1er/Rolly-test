from database import db
from dataclasses import dataclass

@dataclass
class VoterListPoll(db.Model):
  __tablename__ = 'voter_list_poll'
  __table_args__ = {'schema': 'public'}

  voter_list_id: int
  poll_id: int

  voter_list_id = db.Column(db.Integer, db.ForeignKey('public.voter_list.id', ondelete='CASCADE'), primary_key=True)
  poll_id = db.Column(db.Integer, db.ForeignKey('public.poll.id', ondelete='CASCADE'), primary_key=True)

  def __init__(self, voter_list_id, poll_id):
    self.voter_list_id = voter_list_id
    self.poll_id = poll_id
