from database import db
from dataclasses import dataclass

@dataclass
class VoterListMember(db.Model):
  __tablename__ = 'voter_list_member'
  __table_args__ = {'schema': 'public'}

  voter_list_id: int
  user_id: str

  voter_list_id = db.Column(db.Integer, db.ForeignKey('public.voter_list.id', ondelete='CASCADE'), primary_key=True)
  user_id = db.Column(db.String, db.ForeignKey('public.user.id', ondelete='CASCADE'), primary_key=True)

  def __init__(self, voter_list_id, user_id):
    self.voter_list_id = voter_list_id
    self.user_id = user_id
