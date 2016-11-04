# all the imports
import logging
from flask import render_template, Blueprint, Response, jsonify
from debug_modules.selfsold import Selfsold

logger = logging.getLogger('debugTool.log')

bp = Blueprint('debugTool_routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route("/data/debug/<int:adgroup_id>", methods=['GET'])
def all_employees(adgroup_id):
    print adgroup_id
    return jsonify(Selfsold.getDocId(adgroup_id))
