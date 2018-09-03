from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from helloflask.auth import login_required
from helloflask.db import get_db

bp = Blueprint('welcome', __name__)

@bp.route('/')
def welcome():
    return render_template('welcome/index.html')
