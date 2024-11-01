
from flask import * 

blueprint = Blueprint('user', __name__, url_prefix='/user' ,template_folder='templates')

# 로그인 기능
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'bin' and password == '1234':  # 아이디 비밀번호 조회 기능 추가
            session['login_info'] = username  # 로그인 정보 세션에 저장
            flash('로그인 성공!')  # 로그인 성공 메시지
            return redirect(url_for('main.main'))  # => 리디렉션 처리
        else:
            flash('로그인 실패. 사용자 이름 또는 비밀번호를 확인하세요.')  # 오류 메시지
            return redirect(url_for('user.login'))  # 로그인 실패 시 로그인 페이지로 이동
        
    return render_template('login.html')

# 로그아웃
@blueprint.route('/logout')
def logout():
    if 'login_info' in session:
        session.pop('login_info', None)
        flash('로그아웃 되었습니다.')  # 로그아웃 메시지
    return redirect(url_for('main.main'))

# 회원가입
@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')  # 이메일 중복 처리 등 추가적 처리 필요함. 회원가입 완료 뒤에는 로그인 화면으로 리디렉션 되야함
    else:
        return redirect(url_for('main'))

# 마이페이지(이름, ID, 구매 내역, 판매 내역 크레딧 조회 가능하도록)
@blueprint.route('/myPage')
def myPage():
    if 'login_info' in session:
        username = session['login_info']
        return render_template('myPage.html', name=username)
    else:
        return redirect(url_for('user.login'))  # 세션이 없다면 로그인으로

# 구매 내역 페이지(실제 상품 연동 필요)
@blueprint.route('/buyList')
def buyList():
    return render_template('buyList.html')

# 판매 내역 페이지(실제 상품 연동 필요)
@blueprint.route('/sellList')
def sellList():
    return render_template('sellList.html')

# 크레딧 충전 페이지
# 크레딧 충전 완료되면 home으로 리디렉션 되도록 수정필요
@blueprint.route('/addCredit')
def addCredit():
    return render_template('addCredit.html')
