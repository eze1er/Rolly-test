from database import db
from dataclasses import dataclass

@dataclass
class Answer(db.Model):
  __tablename__ = 'answer'
  __table_args__ = {'schema': 'public'}

  id: int
  poll_id: str
  content: str

  id = db.Column(db.Integer, primary_key=True)
  poll_id = db.Column(db.Integer, db.ForeignKey('public.poll.id', ondelete='CASCADE'), nullable=False)
  content = db.Column(db.Text)

  # list of votes for answer
  votes = db.relationship('Vote', cascade='all, delete')

  def __init__(self, poll_id, content):
    self.poll_id = poll_id
    self.content = content
