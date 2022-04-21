from database import db
from dataclasses import dataclass

@dataclass
class VoterList(db.Model):
  __tablename__ = 'voter_list'
  __table_args__ = {'schema': 'public'}

  id: int
  user_id: str
  name: str

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.String, db.ForeignKey('public.user.id', ondelete='CASCADE'), nullable=False)
  name = db.Column(db.String, nullable=False)

  # list of members of email list
  voter_list_members = db.relationship('VoterListMember', cascade='all, delete')
  # list of polls for email list
  voter_list_polls = db.relationship('VoterListPoll', cascade='all, delete')


  def __init__(self, user_id, name):
    self.user_id = user_id
    self.name = name
