import pymysql

class db_connection:
    def __init__(self):
        pass
    
		# DB 연결
		# Connection을 반환하는 메서드
		# 클래스메서드는 인스턴스 생성 없이 호출 가능: db_connection.get_db()
    @classmethod
    def get_db(self):
        return pymysql.connect(
            host='localhost',
            user='root',
            password='rnrtmdqls98!',
            db='project',
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
        curs = conn.cursor()
        sql = "SELECT * FROM users WHERE user_id = %s"
        curs.execute(sql, (user_id,))
        user = curs.fetchone()
        conn.close()
        return user


# 클래스 수정해서 사용
        
if __name__ == '__main__':
    # 새로운 UserDao 테스트 코드
    user = UserDao().get_user('test_user@example.com', 'test_password') # 확인용
    if user:
        print(f"User found: {user}")
    else:
        print("User not found")
    