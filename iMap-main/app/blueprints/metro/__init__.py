from app import constants
from flask import current_app, redirect, render_template, Blueprint, request, jsonify, url_for

bp_metro = Blueprint(
    'metro',
    __name__,
    template_folder='templates',
    url_prefix='/metro'
)

@bp_metro.route('/', methods = ["GET", "POST"])
def metro():
    return render_template("metro.html", constants = constants)
