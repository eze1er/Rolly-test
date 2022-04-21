import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from app import app
from models.User import User
from models.Poll import Poll
from models.Vote import Vote
from models.VoterList import VoterList
from models.Answer import Answer
import datetime

import random
import names
import pandas as pd

AGE_MAX = 100
AGE_MIN = 18
POLL_RADIUS_MAX = 200
POLL_RADIUS_MIN = 150

def get_random_date(start, end, input_format, output_format):
    format = '%Y-%m-%d'
    stime = datetime.datetime.strptime(start, input_format)
    etime = datetime.datetime.strptime(end, input_format)
    td = etime - stime
    return (random.random() * td + stime).strftime(output_format)

def load_sample_values(filename):
  df = pd.read_csv(filename, delimiter=',')
  # remove nan values and return as dict
  return {df[column].name: [y for y in df[column] if not pd.isna(y)] for column in df}

def load_polls(filename):
  df = pd.read_csv(filename, delimiter=',')
  return df.groupby(['Poll', 'Category', 'Description']).apply(lambda s: s[['Answer']].to_dict(orient='records')).to_dict()


def create_user(email, LATITUDE_MIN, LATITUDE_MAX, LONGITUDE_MIN, LONGITUDE_MAX):
  user = User(email)
  user.gender = random.choice(sample_values['Gender'])
  user.first_name = names.get_first_name(gender = user.gender.lower())
  user.last_name = names.get_last_name()
  user.longitude = random.uniform(LONGITUDE_MIN, LONGITUDE_MAX)
  user.latitude = random.uniform(LATITUDE_MIN, LATITUDE_MAX)
  user.age = random.randint(AGE_MIN,AGE_MAX)
  user.ethnicity = random.choice(sample_values['Ethnicity'])
  user.industry = random.choice(sample_values['Industry'])
  user.religion = random.choice(sample_values['Religion'])
  user.income_range = random.choice(sample_values['Income range'])
  user.education = random.choice(sample_values['Education'])
  user.marital_status = random.choice(sample_values['Marital status'])
  user.veteran = random.random() < 0.01

  return user

def create_poll(email, name, category, description, LATITUDE_MIN, LATITUDE_MAX, LONGITUDE_MIN, LONGITUDE_MAX, REGION):
  poll = Poll(
    email,
    category,
    name,
    REGION,
    False,
    description,
    get_random_date('2020-01-01','2021-01-01','%Y-%m-%d', '%Y-%m-%d'),
    get_random_date('2021-01-02','2022-01-01','%Y-%m-%d', '%Y-%m-%d'),
    random.uniform(LONGITUDE_MIN, LONGITUDE_MAX),
    random.uniform(LATITUDE_MIN, LATITUDE_MAX),
    random.randint(POLL_RADIUS_MIN, POLL_RADIUS_MAX),
    True)

  return poll


def populate_database_with_coordinates(LATITUDE_MIN, LATITUDE_MAX, LONGITUDE_MIN, LONGITUDE_MAX, REGION):
  REGION_NAME = REGION.replace(' ', '').lower()

  with app.app_context():
    # create voters who will only vote on answers
    for v in range(0, 100):
      user = create_user(f'voter_{REGION_NAME}_{v}@email.com', LATITUDE_MIN, LATITUDE_MAX, LONGITUDE_MIN, LONGITUDE_MAX)
      db.session.add(user)
      db.session.commit()

    poll_count = 0
    for poll, answers in polls.items():
      # create user and poll owned by the user
      user = create_user(f'owner_{REGION_NAME}_{poll_count}@email.com', LATITUDE_MIN, LATITUDE_MAX, LONGITUDE_MIN, LONGITUDE_MAX)
      poll = create_poll(f'owner_{REGION_NAME}_{poll_count}@email.com', poll[0], poll[1], poll[2], LATITUDE_MIN, LATITUDE_MAX, LONGITUDE_MIN, LONGITUDE_MAX, REGION)

      poll_count += 1

      # 75% chance to have a non-expired poll
      if(random.random() < 0.75):
        poll.end_at = get_random_date('2023-01-01','2024-01-01','%Y-%m-%d', '%Y-%m-%d')

      db.session.add(poll)
      db.session.add(user)
      db.session.flush()

      # create answers
      answer_ids = []
      for answer_item in answers:
        answer = Answer(poll.id, answer_item['Answer'])
        db.session.add(answer)
        db.session.flush()
        answer_ids.append(answer.id)

      # for each answer_id, generate a random weighting
      weighting = []
      for j in answer_ids:
        weighting.append(random.random())

      # generate a list of answer_ids to vote on with a random length
      answer_ids_to_vote_on = random.choices(answer_ids, weights=weighting, k=random.randint(50,100))

      # vote with random number of voters with a random weighting
      voter_num = 0
      for answer_id in answer_ids_to_vote_on:
        vote = Vote(f'voter_{REGION_NAME}_{voter_num}@email.com', poll.id, answer_id)
        voter_num+=1
        db.session.add(vote)

    db.session.commit()

# drop tables if exist
# create all tables
with app.app_context():
  db.drop_all()
  db.create_all()

# load sample values for each property from csv file
sample_values = load_sample_values('tools/dbsamplevalues.csv')
polls = load_polls('tools/polls.csv')

# Sydney
populate_database_with_coordinates(-33.918015, -33.757231, 150.956441, 151.248958, 'Oceania')

# London
populate_database_with_coordinates(51.380099, 51.575968, -0.276916, 0.046813, 'Europe')

# Nairobi
populate_database_with_coordinates(-1.336352, -1.235159, 36.732246, 36.901376, 'Africa')

# Sao Paolo
populate_database_with_coordinates(-23.633941, -23.448576, -46.754080, -46.497701, 'South America')

# Singapore
populate_database_with_coordinates(1.309941, 1.412909, 103.76105, 103.897682, 'Asia')

# Toronto
populate_database_with_coordinates(43.755408, 43.914581, -79.688323, -79.189666, 'North America')
