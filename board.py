from flask import *
from projectDB import *

blueprint = Blueprint('board', __name__, url_prefix='/board' ,template_folder='templates')

# 게시판 페이지(ID, 게시글, 작성 시간, 댓글)
@blueprint.route('/view')
def view():
    posts = PostDao().get_all_posts()  # 모든 게시글 조회
    return render_template('board.html', posts=posts)

# 게시글 추가 페이지, Insert 추가 처리 필요
@blueprint.route('/newPost', methods=['GET', 'POST'])
def newPost():
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
        return render_template('viewPost.html', post=post)
    else:
        flash('해당 게시글을 찾을 수 없습니다.')
        return redirect(url_for('board.view'))
