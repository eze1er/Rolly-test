from flask import Flask
from database import db
from flask_migrate import Migrate
from flask_cors import CORS


from routes.poll_bp import poll_bp
from routes.user_bp import user_bp
from routes.vote_bp import vote_bp
from routes.voter_list_bp import voter_list_bp


app = Flask(__name__)
app.config.from_object('config')
app.url_map.strict_slashes = False


cors = CORS(app)


db.init_app(app)
migrate = Migrate(app, db)


app.register_blueprint(poll_bp, url_prefix='/poll')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(vote_bp, url_prefix='/vote')
app.register_blueprint(voter_list_bp, url_prefix='/voterlist')


@app.route('/', methods=['GET'])
def index():
  return 'Welcome to Mapocracy API'


if __name__ == '__main__':
  app.run()
