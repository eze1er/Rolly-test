from database import db
from dataclasses import dataclass
from datetime import datetime

# many to many association object
@dataclass
class Vote(db.Model):
  __tablename__ = 'vote'
  __table_args__ = {'schema': 'public'}

  user_id: str
  poll_id: int
  answer_id: int
  voted_at: datetime

  user_id = db.Column(db.String, db.ForeignKey('public.user.id', ondelete='CASCADE'), primary_key=True)
  poll_id = db.Column(db.Integer, db.ForeignKey('public.poll.id', ondelete='CASCADE'), primary_key=True)
  answer_id = db.Column(db.Integer, db.ForeignKey('public.answer.id', ondelete='CASCADE'), nullable=False)
  voted_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

  def __init__(self, user_id, poll_id, answer_id):
    self.user_id = user_id
    self.poll_id = int(poll_id)
    self.answer_id = int(answer_id)
