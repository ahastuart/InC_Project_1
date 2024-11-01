from flask import *

blueprint = Blueprint('product', __name__, url_prefix='/product' ,template_folder='templates')

# 상품 등록 페이지
# 상품 등록 되지 않음. 수정 필요
@blueprint.route('/addProduct', methods=['GET', 'POST'])
def addProduct():
    if request.method == 'POST':
        product_name = request.form['productName']
        product_description = request.form['productDescription']
        product_image = request.form['productImage']
        
        # 상품 정보를 딕셔너리로 만들어 리스트에 추가
        products.append({
            'name': product_name,
            'description': product_description,
            'image': product_image
        })
        # CDN, DB에는 경로만 사진은 로컬에
        
        flash('상품이 등록되었습니다!')  # 등록 성공 메시지
        return redirect(url_for('main.main'))  # 메인 화면으로 리디렉션

    return render_template('addProduct.html')

# 구매 페이지(이미지, 크레딧 차감 처리, 결제 완료 후에는 이미지 판매완료 처리, 구매자 PK 포함)
@blueprint.route('/buyProduct')
def buyProduct():
    return render_template('buyProduct.html')

# 생성 페이지
@blueprint.route('/createImage')
def createImage():
    return render_template('createImage.html')

# 프롬프트를 통한 이미지 생성
@blueprint.route('/generateImageFromPrompt')
def generateImageFromPrompt():
    pass # 이미지 완성 후 저장 페이지로 이동

# 카테고리를 이용한 이미지 생성
@blueprint.route('/generateImageFromCategory')
def generateImageFromCategory():
    pass # 이미지 완성 후 저장 페이지로 이동

# 이미지 생성 후 저장 페이지 추가 필요
@blueprint.route('/route_name')
def method_name():
    pass
