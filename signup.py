from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash
from projectDB import UserDao

blueprint = Blueprint('signup', __name__)

@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form['UserName']
        id = request.form['UserId']
        password = request.form['UserPw']
        confirm_password = request.form['UserPwConfirm']

        if password != confirm_password:
            flash('비밀번호가 일치하지 않습니다.')
            return redirect(url_for('signup.signup'))

        user_dao = UserDao()
        existing_user = user_dao.get_user_by_id(id)
        if existing_user:
            flash('이미 사용 중입니다. 다른 값을 넣어주세요.')
            return redirect(url_for('signup.signup'))

        hashed_password = generate_password_hash(password)
        result = user_dao.insert_user(user_name, id, hashed_password)
        
        if 'Insert OK' in result:
            flash('회원가입이 완료되었습니다.')
            return redirect(url_for('user.login'))
        else:
            flash('FATAL ERROR !')
            return redirect(url_for('signup.signup'))

    return render_template('signup.html')

@blueprint.route('/check_duplicate', methods=['POST'])
def check_duplicate():
    data = request.get_json()
    user_id = data.get('userId')
    
    user_dao = UserDao()
    existing_user = user_dao.get_user_by_id(user_id)
    
    is_duplicate = existing_user is not None
    
    return jsonify({'isDuplicate': is_duplicate})