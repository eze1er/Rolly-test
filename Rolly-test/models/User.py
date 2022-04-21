from database import db
from dataclasses import dataclass

@dataclass
class User(db.Model):
  __tablename__ = 'user'
  __table_args__ = {'schema': 'public'}

  id: str
  first_name: str
  last_name: str
  longitude: float
  latitude: float
  age: int
  gender: str
  ethnicity: str
  industry: str
  religion: str
  income_range: str
  education: str
  marital_status: str
  veteran: bool

  id = db.Column(db.String, primary_key=True)
  first_name = db.Column(db.String, default='')
  last_name = db.Column(db.String, default='')
  longitude = db.Column(db.Numeric)
  latitude = db.Column(db.Numeric)
  age = db.Column(db.Integer)
  gender = db.Column(db.String, default='')
  ethnicity = db.Column(db.String, default='')
  industry = db.Column(db.String, default='')
  religion = db.Column(db.String, default='')
  income_range = db.Column(db.String, default='')
  education = db.Column(db.String, default='')
  marital_status = db.Column(db.String, default='')
  veteran = db.Column(db.Boolean, default=False)

  # list of polls for user
  polls = db.relationship(
    'Poll',
    cascade='all, delete',
    order_by='desc(Poll.id)'
  )
  # list of votes for user
  votes = db.relationship('Vote', cascade='all, delete')
  # list of email lists owned by user
  voter_lists = db.relationship('VoterList', cascade='all, delete')
  # list of email lists user is member of
  voter_list_membership = db.relationship('VoterListMember', cascade='all, delete')

  def __init__(self, email):
    self.id = email
