from flask import Blueprint
from controllers.UserController import *

user_bp = Blueprint('user_bp', __name__)

user_bp.route('/', methods=['GET'])(index)
user_bp.route('/<user_id>', methods=['GET'])(get_user_by_email)
user_bp.route('/<user_id>/poll', methods=['GET'])(get_user_poll)
user_bp.route('/<user_id>/invites', methods=['GET'])(get_user_invites)
user_bp.route('/<user_id>/voterlist', methods=['GET'])(get_user_voter_list)
user_bp.route('/new', methods=['POST'])(create_user)
user_bp.route('/update', methods=['PUT'])(update_user)
