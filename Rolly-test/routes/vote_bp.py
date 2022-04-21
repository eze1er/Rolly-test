from flask import Blueprint
from controllers.VoteController import *

vote_bp = Blueprint('vote_bp', __name__)

vote_bp.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])(index)
