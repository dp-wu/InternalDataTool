from flask import Blueprint, render_template


bp = Blueprint('auth', __name__)

@bp.route('/')
def index():
    return 'Auth Page'
