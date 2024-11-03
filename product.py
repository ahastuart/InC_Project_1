from flask import *
from gpt_dalle_module import *
import os
from PIL import Image
from io import BytesIO
import base64

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

# 이미지 생성 바로 저장되도록 해서 이미지 저장버튼 처리 필요없음

# 프롬프트를 통한 이미지 생성
@blueprint.route('/generateImageFromPrompt', methods=['GET', 'POST'])
def generateImageFromPrompt():
    # 프롬프트에 입력한 내용을 GPT를 통해 DALL-E 프롬프트로 만들고, 이를 DALL-E에게 주입시켜 이미지를 생성한 후 created 페이지로 리턴해야 함
    if request.method == 'POST':
        user_prompt = request.form.get('prompt')
        user_id = session.get('user_id')
        
        if not user_prompt:
            flash('프롬프트를 입력해주세요')
            return redirect(url_for('product.createImage'))
        
        # 크레딧 감소 시도
        if not productDAO().generate_image(user_id):
            flash('크레딧이 부족하여 이미지를 생성할 수 없습니다.')
            return redirect(url_for('product.createImage'))

        dalle_propt = generate_dalle_prompt(user_prompt)
        
        image_data = create_dalle_image(dalle_propt)
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        
        # 이미지는 로컬에 저장됨. 
        filename = f'{user_id}_image_{user_prompt[:10]}.png'
        save_path = os.path.join('/static/generated_image', filename)
        image.save(save_path)
        
        image_url = url_for('static', filename=f'generated_image/{filename}')
        return redirect(url_for('product.generatedImage', image_url=image_url))

    if request.method == 'GET':
        return render_template('createIamge.html')
    
    
# 카테고리를 이용한 이미지 생성
@blueprint.route('/generateImageFromCategory', methods=['GET', 'POST'])
def generateImageFromCategory():
    if request.method == 'POST':
        
        category = request.form.get('category')
        topic = request.form.get('topic')
        user_id = session.get('user_id')
        
        if not category or not topic:
            flash('프롬프트를 입력해주세요')
            return redirect(url_for('product.createImage'))
        
        # 크레딧 감소 시도
        if not productDAO().generate_image(user_id):
            flash('크레딧이 부족하여 이미지를 생성할 수 없습니다.')
            return redirect(url_for('product.createImage'))
        
        prompt = generate_dalle_category(category, topic)
        
        image_data = create_dalle_image(prompt)
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        
        filename = f'{user_id}_image_{topic}.png' # 파일 이름 수정완료
        save_path = os.path.join(current_app.root_path, 'static', 'generated_image', filename)
        image.save(save_path)
        
        image_url = url_for('static', filename=f'generated_image/{filename}')
        return redirect(url_for('product.generatedImage', image_url=image_url))
    
    if request.method == 'GET':
        return render_template('createImage.html')
    

# 생성된 이미지 결과 화면. 이미지 생성 시 image에 저장되도록 했기 때문에 추가로 저장은 필요 없음
@blueprint.route('/createdImage')
def generatedImage():
    image_url = request.args.get('image_url')
    return render_template('createdImage.html', image_url=image_url)
