from database import db
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy.orm import joinedload


@dataclass
class Poll(db.Model):
  __tablename__ = 'poll'
  __table_args__ = {'schema': 'public'}

  id: int
  user_id: str
  category: str
  name: str
  region: str
  restriction: bool
  description: str
  created_at: datetime
  start_at: datetime
  end_at: datetime
  longitude: float
  latitude: float
  radius: int
  center: str
  visibility: bool

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.String, db.ForeignKey('public.user.id', ondelete='CASCADE'), nullable=False)
  category = db.Column(db.String)
  name = db.Column(db.String, nullable=False)
  region = db.Column(db.String)
  restriction = db.Column(db.Boolean)
  description = db.Column(db.Text)
  created_at = db.Column(db.DateTime, nullable=False)
  start_at = db.Column(db.DateTime, nullable=False)
  end_at = db.Column(db.DateTime, nullable=False)
  longitude = db.Column(db.Float(asdecimal=False, decimal_return_scale=None))
  latitude = db.Column(db.Float(asdecimal=False, decimal_return_scale=None))
  radius = db.Column(db.Integer)
  center = db.Column(db.String)
  visibility = db.Column(db.Boolean)

  # list of answers for poll
  answers = db.relationship('Answer', cascade='all, delete', lazy='joined')
  # list of voter lists for poll
  voter_lists = db.relationship('VoterListPoll', cascade='all, delete', lazy='joined')


  def __init__(self, user_id, category, name, region, restriction, description, start_at, end_at, longitude, latitude, radius, visibility):
    self.user_id = user_id
    self.category = category
    self.name = name
    self.region = region
    self.restriction = restriction
    self.description = description
    self.created_at = datetime.now()
    self.start_at = datetime.strptime(start_at, '%Y-%m-%d')
    self.end_at = datetime.strptime(end_at, '%Y-%m-%d')
    self.longitude = longitude
    self.latitude = latitude
    self.radius = radius
    self.center = f'[{str(self.latitude)}, {str(self.longitude)}]'
    self.visibility = visibility

  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}
