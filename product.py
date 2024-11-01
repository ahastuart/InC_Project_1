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
        
        if not user_prompt:
            flash('프롬프트를 입력해주세요')
            return redirect(url_for('product.createImage'))

        dalle_propt = generate_dalle_prompt(user_prompt)
        
        image_data = create_dalle_image(dalle_propt)
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        
        filename = f'{username}_image_{product_id}.png' # 번호 어떻게 부여할지 고민
        save_path = os.path.join('/static/generated_image', filename)
        image.save(save_path)
        
        return redirect(url_for('product.generatedImage')) # 이미지 완성 후 저장 페이지로 이동

    if request.method == 'GET':
        return render_template('createIamge.html')
    
    
# 카테고리를 이용한 이미지 생성
@blueprint.route('/generateImageFromCategory', methods=['GET', 'POST'])
def generateImageFromCategory():
    if request.method == 'POST':
        
        category = request.form.get('category')
        topic = request.form.get('topic')
        
        if not category or not topic:
            flash('프롬프트를 입력해주세요')
            return redirect(url_for('product.createImage'))
        
        prompt = generate_dalle_category(category, topic)
        
        image_data = create_dalle_image(prompt)
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        
        #filename = f'{username}_image_{product_id}.png' # 번호 어떻게 부여할지 고민
        filename = '1.png'
        # save_path = os.path.join('/static/generated_image', filename)
        save_path = os.path.join(current_app.root_path, 'static', 'generated_image', filename)
        image.save(save_path)
        
        
        return redirect(url_for('product.generatedImage'))
    
    if request.method == 'GET':
        return render_template('createImage.html')
    

# 생성하자마자 저장되도록 구현해서 저장 기능 필요 없음. DB에서 받아서 보여주는 기능만 수행하면 됨. 다시 만들기는 생성페이지로 리디렉션 되도록
# 이미지 생성 후 저장 페이지 추가 필요  -> 이미지를 저장하는 기능을 수행할 수 있도록 해야함. 저장하기를 누르면 이미지 폴더에 자동으로 저장이 되도록
@blueprint.route('/generatedImage')
def generatedImage():
    return render_template('createdImage.html')
