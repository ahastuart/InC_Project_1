from flask import *
from projectDB import *

blueprint = Blueprint('main', __name__, template_folder='templates')

# 초기 화면
@blueprint.route('/')
def index():
    return redirect(url_for('main.main'))

# 메인 화면
@blueprint.route('/main')
def main():
    # DB에서 상품 목록 가져오기
    product_dao = productDAO()
    products = product_dao.get_all_products()  # DB에서 모든 상품 정보를 가져옵니다.
    return render_template('home.html', products=products)  # 'products'를 템플릿으로 전달
