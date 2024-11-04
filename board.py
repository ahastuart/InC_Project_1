from flask import *
from projectDB import *

blueprint = Blueprint('board', __name__, url_prefix='/board' ,template_folder='templates')

# 게시판 페이지(ID, 게시글, 작성 시간, 수정 시간)
@blueprint.route('/view')
def view():
    posts = PostDao().get_all_posts()  # 모든 게시글 조회
    return render_template('board.html', posts=posts)

# 게시글 추가 페이지
@blueprint.route('/newPost', methods=['GET', 'POST'])
def newPost():
    # 로그인 상태 확인
    if 'user_id' not in session:
        flash('로그인 후에 게시글을 작성할 수 있습니다.')
        return redirect(url_for('user.login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = session.get('user_id')
        
        if user_id:  # 사용자가 로그인된 경우
            PostDao().insert_post(user_id, title, content)
            flash('게시글이 성공적으로 작성되었습니다.')
            return redirect(url_for('board.view'))
        else:
            flash('로그인 후에 게시글을 작성할 수 있습니다.')
            return redirect(url_for('user.login'))
    return render_template('newPost.html')


# 게시글 조회 페이지 select 추가 처리 필요
@blueprint.route('/viewPost/<int:post_id>')
def viewPost(post_id):
    post = PostDao().get_post_by_id(post_id)
    if post:
        user_name = UserDao().get_user_by_id(post['user_id'])['user_name']
        return render_template('viewPost.html', post=post, user_name=user_name)
    else:
        flash('해당 게시글을 찾을 수 없습니다.')
        return redirect(url_for('board.view'))
    
# 게시글 수정 페이지
@blueprint.route('/editPost/<int:post_id>', methods=['GET', 'POST'])
def editPost(post_id):
    post = PostDao().get_post_by_id(post_id)
    
    # 게시글이 존재하는지 확인
    if not post:
        flash('해당 게시글을 찾을 수 없습니다.')
        return redirect(url_for('board.view'))
    
    # 수정 요청 처리
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        PostDao().update_post(post_id, new_title, new_content)
        flash('게시글이 성공적으로 수정되었습니다.')
        return redirect(url_for('board.viewPost', post_id=post_id))
    
    return render_template('editPost.html', post=post)
