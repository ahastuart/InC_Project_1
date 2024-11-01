from flask import *

blueprint = Blueprint('board', __name__, url_prefix='/board' ,template_folder='templates')

# 게시판 페이지(ID, 게시글, 작성 시간, 댓글)
@blueprint.route('/view')
def view():
    return render_template('board.html')

# 게시글 추가 페이지, Insert 추가 처리 필요
@blueprint.route('/newPost')
def newPost():
    return render_template('newPost.html')

# 게시글 조회 페이지 select 추가 처리 필요
@blueprint.route('/viewPost')
def viewPost():
    return render_template('viewPost.html')
