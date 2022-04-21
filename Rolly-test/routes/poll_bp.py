from flask import Blueprint
from controllers.PollController import *


poll_bp = Blueprint('poll_bp', __name__)


poll_bp.route('/', methods=['GET'])(filter_polls)
poll_bp.route('/<int:id>', methods=['GET'])(get_poll_by_id)
poll_bp.route('/new', methods=['POST'])(create_poll)
poll_bp.route('/update', methods=['PUT'])(update_poll)
