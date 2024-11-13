from flask import Blueprint, render_template
from flask_login import login_required

pos_bp = Blueprint('pos', __name__)


@pos_bp.route('/pos', methods=['GET'])
@login_required
def pos():
    return render_template('pos/pos.html')
