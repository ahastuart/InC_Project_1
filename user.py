
from flask import * 
from projectDB import *

blueprint = Blueprint('user', __name__, url_prefix='/user' ,template_folder='templates')

# 로그인 기능
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 사용자 정보 조회
        user = UserDao().get_user(username, password)

        if user:  # 사용자가 존재할 경우
            session['login_info'] = user[1]  # 로그인 정보 세션에 저장
            session['user_id'] = user[0]  # 사용자 고유 ID 저장
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
        session.pop('user_id', None)
        flash('로그아웃 되었습니다.')  # 로그아웃 메시지
    return redirect(url_for('main.main'))

# 회원가입
@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form['UserName']
        id = request.form['UserId']
        password = request.form['UserPw']
        confirm_password = request.form['UserPwConfirm']

        if password != confirm_password:
            flash('비밀번호가 일치하지 않습니다.')
            return redirect(url_for('user.signup'))

        user_dao = UserDao()
        existing_user = user_dao.get_user_by_id(id)
        if existing_user:
            flash('이미 사용 중입니다. 다른 값을 넣어주세요.')
            return redirect(url_for('user.signup'))

        result = user_dao.insert_user(user_name, id, password)
        
        if 'Insert OK' in result:
            flash('회원가입이 완료되었습니다.')
            return redirect(url_for('user.login'))
        else:
            flash('FATAL ERROR !')
            return redirect(url_for('user.main'))

    return render_template('signup.html')

# id 중복 확인
@blueprint.route('/check_duplicate', methods=['POST'])
def check_duplicate():
    data = request.get_json()
    id = data.get('UserId')
    
    user_dao = UserDao()
    existing_user = user_dao.get_user_by_id(id)
    is_duplicate = existing_user is not None
    
    return jsonify({'isDuplicate': is_duplicate})

# # 회원가입 세부 기능
# @blueprint.route('/register')
# def register():
#     pass


# # 회원가입 세부 기능
# @blueprint.route('/register')
# def register():
#     pass


# 마이페이지(이름, ID, 구매 내역, 판매 내역 크레딧 조회 가능하도록)
@blueprint.route('/myPage')
def myPage():
    if 'login_info' in session:
        username = session['login_info']
        user_id = session['user_id']
        user = UserDao().get_user_by_id(user_id)
        if user:
            user_data = {
                'name': user['user_name'],
                'email': user['id'],
                'signup_date': user['signup_date'],
                'credit': user['credit']
            }
        return render_template('myPage.html', user_data=user_data)
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
