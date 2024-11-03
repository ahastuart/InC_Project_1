import pymysql
import datetime

class db_connection:
    def __init__(self):
        pass
    
		# DB 연결
		# Connection을 반환하는 메서드
		# 클래스메서드는 인스턴스 생성 없이 호출 가능: db_connection.get_db()
    @classmethod
    def get_db(self):
        # return pymysql.connect(
        #     host='localhost',
        #     user='root',
        #     password='rnrtmdqls98!',
        #     db='project',
        #     charset='utf8',
        #     autocommit=True  # 테스트환경에서는 이렇게 사용
        # )
        return pymysql.connect(
            host='localhost',
            user='newuser',
            password='qwer1234',
            db='mini1',
            charset='utf8',
            autocommit=True  # 테스트환경에서는 이렇게 사용
        )

class UserDao:
    def __init__(self):
        pass
    
    # 사용자 조회
    def get_user(self, id, password):
        conn = db_connection.get_db()
        curs = conn.cursor()
        sql = "SELECT * FROM users WHERE id = %s AND password = %s"
        curs.execute(sql, (id, password))
        user = curs.fetchone()
        conn.close()
        return user
    
    # 사용자 정보 ID로 조회 (마이페이지에서 사용)
    def get_user_by_id(self, user_id):
        conn = db_connection.get_db()
        curs = conn.cursor(pymysql.cursors.DictCursor)  # DictCursor 사용
        sql = "SELECT * FROM users WHERE user_id = %s"
        curs.execute(sql, (user_id,))
        user = curs.fetchone()
        conn.close()
        return user


class PostDao:
    def __init__(self):
        pass
    
    # 모든 게시글 조회
    def get_all_posts(self):
        conn = db_connection.get_db()
        curs = conn.cursor(pymysql.cursors.DictCursor)  # DictCursor 사용
        sql = "SELECT * FROM posts ORDER BY created_at DESC"
        curs.execute(sql)
        posts = curs.fetchall()
        conn.close()
        return posts

    # 게시글 ID로 조회
    def get_post_by_id(self, post_id):
        conn = db_connection.get_db()
        curs = conn.cursor(pymysql.cursors.DictCursor)  # DictCursor 사용
        sql = "SELECT post_id, user_id, title, content, created_at FROM posts WHERE post_id = %s"
        curs.execute(sql, (post_id,))
        post = curs.fetchone()
        conn.close()
        return post

    # 게시글 추가
    def insert_post(self, user_id, title, content):
        conn = db_connection.get_db()
        curs = conn.cursor()
        sql = "INSERT INTO posts (user_id, title, content, created_at) VALUES (%s, %s, %s, %s)"
        curs.execute(sql, (user_id, title, content, datetime.datetime.now()))
        conn.commit()
        conn.close()

    # 게시글 수정
    def update_post(self, post_id, new_title, new_content):
        conn = db_connection.get_db()
        curs = conn.cursor()
        sql = "UPDATE posts SET title = %s, content = %s, updated_at = NOW() WHERE post_id = %s"
        curs.execute(sql, (new_title, new_content, post_id))
        conn.commit()
        conn.close()

# 상품 관련 DB
class productDAO:
    def __init__(self):
        pass
    
    # 상품 추가
    def add_product(self, product_name, description, image_path, price, user_id):
        conn = db_connection.get_db()
        curs = conn.cursor()
        add_sql = '''
        INSERT INTO products (product_name, description, image_path, price, user_id)
                VALUES (%s, %s, %s, %s, %s)
        '''
        curs.execute(add_sql, (product_name, description, image_path, price, user_id))
        curs.close()

    # user_id로 상품 조회
    def get_products_by_user_id(self, user_id):
        conn = db_connection.get_db()
        curs = conn.cursor()
        sql = 'SELECT * FROM products WHERE user_id = %s'
        curs.execute(sql, (user_id,))
        curs.close()
    
    # 상품 삭제
    def delete_product(self, product_id):
        conn = db_connection.get_db()
        curs = conn.cursor()
        sql = 'DELETE FROM products WHERE product_id = %s'
        curs.execute(sql, (product_id,))
        curs.close()
    
    # 상품 수정
    def update_product(self, product_id, **kwargs):
        conn = db_connection.get_db()
        curs = conn.cursor()
        fields = ', '.join([f'{key} = %s' for key in kwargs.keys()])
        sql = f'UPDATE products SET {fields} WHERE product_id = %s'
        values = list(kwargs.values()) + [product_id]
        curs.execute(sql, values)
        curs.close()
        
    # 상품 생성 시 크레딧 500 감소하도록 처리
    def generate_image(self,user_id):
        conn = db_connection.get_db()
        curs = conn.cursor()
        # 추가될 때 크레딧 감소시켜야 함
        update_sql = '''
        UPDATE users
        SET credit = credit - 500
        WHERE user_id = %s AND credit >= 500
        '''
        curs.execute(update_sql,(user_id,))
        curs.close()
    
# 클래스 수정해서 사용
        
if __name__ == '__main__':
    # 새로운 UserDao 테스트 코드
    user = UserDao().get_user('test_user@example.com', 'test_password') # 확인용
    if user:
        print(f"User found: {user}")
    else:
        print("User not found")
    