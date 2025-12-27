from flask import Blueprint, render_template


query_bp = Blueprint('query', __name__)

@query_bp.route('/')
def index():
    return 'Query Page'
