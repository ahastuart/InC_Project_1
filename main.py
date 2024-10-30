from flask import *

# 기능 별 분리 생각할것
# 알케미, 블루프린트 추가하기
# 검색기능 추가, 카테고리별 보기 및 검색
# streamlit

app = Flask(__name__)
app.secret_key = 'bsdajvkbakjbfoehihewrpqkldn21pnifninelfbBBOIQRqnflsdnljneoBBOBi2rp1rp12r9uh'

# 초기 화면
@app.route('/')
def index():
    return redirect(url_for('main'))

# 메인 화면
@app.route('/main')
def main():
    return render_template('home.html')

# 로그인 기능
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'bin' and password == '1234':  # 아이디 비밀번호 조회 기능 추가
            session['login_info'] = username  # 로그인 정보 세션에 저장
            flash('로그인 성공!')  # 로그인 성공 메시지
            return redirect(url_for('main'))  # => 리디렉션 처리
        else:
            flash('로그인 실패. 사용자 이름 또는 비밀번호를 확인하세요.')  # 오류 메시지
            return render_template('login.html')  # 로그인 실패 시 로그인 페이지로 이동
    return render_template('login.html')

# 로그아웃
@app.route('/logout')
def logout():
    if 'login_info' in session:
        session.pop('login_info', None)
        flash('로그아웃 되었습니다.')  # 로그아웃 메시지
    return redirect(url_for('main'))

# 회원가입
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')  # 이메일 중복 처리 등 추가적 처리 필요함. 회원가입 완료 뒤에는 로그인 화면으로 리디렉션 되야함
    else:
        return redirect(url_for('main'))

# 마이페이지(이름, ID, 구매 내역, 판매 내역 크레딧 조회 가능하도록)
@app.route('/myPage')
def myPage():
    if 'login_info' in session:
        username = session['login_info']
        return render_template('myPage.html', name=username)
    else:
        return redirect(url_for('login'))  # 세션이 없다면 로그인으로
    
# 구매 내역 페이지

# 판매 내역 페이지

# 크레딧 충전 페이지

# 상품 목록을 저장하기 위한 리스트
products = []

# 상품 등록 페이지
# 상품 등록 되지 않음. 수정 필요
@app.route('/addProduct', methods=['GET', 'POST'])
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
        return redirect(url_for('main'))  # 메인 화면으로 리디렉션

    return render_template('addProduct.html')

# 게시판 페이지(ID, 게시글, 작성 시간, 댓글)
@app.route('/board')
def board():
    pass

# 구매 페이지(이미지, 크레딧 차감 처리, 결제 완료 후에는 이미지 판매완료 처리, 구매자 PK 포함)
@app.route('/buyProduct')
def buyProduct():
    pass

# 생성 페이지
@app.route('/createImage')
def createImage():
    pass

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
