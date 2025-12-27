from flask import Blueprint, render_template


bp = Blueprint('query', __name__)

@bp.route('/')
def index():
    return 'Query Page'
