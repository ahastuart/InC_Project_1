from flask import *

blueprint = Blueprint('main', __name__, template_folder='templates')

# 초기 화면
@blueprint.route('/')
def index():
    return redirect(url_for('main.main'))

# 메인 화면
@blueprint.route('/main')
def main():
    return render_template('home.html')
