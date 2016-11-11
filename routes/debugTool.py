# all the imports
import logging
from flask import render_template, Blueprint
from debug_modules.selfsold import Selfsold
from debug_modules.budget import Budget

logger = logging.getLogger('debugTool.log')

bp = Blueprint('debugTool_routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route("/data/selfsold/<int:adgroup_id>", methods=['GET'])
def debugSefsold(adgroup_id):
    return Selfsold.selfsold(adgroup_id)

@bp.route("/data/budget/<int:adgroup_id>", methods=['GET'])
def debugBudget(adgroup_id):
    return Budget.budget(adgroup_id)
