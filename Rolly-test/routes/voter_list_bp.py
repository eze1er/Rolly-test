from flask import Blueprint
from controllers.VoterListController import index, create_voter_list

voter_list_bp = Blueprint('voter_list_bp', __name__)

voter_list_bp.route('/', methods=['GET'])(index)
voter_list_bp.route('/new', methods=['POST'])(create_voter_list)
