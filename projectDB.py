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

# 클래스 수정해서 사용
class DeptDao:
    def __init__(self):
        pass
    
    # SELECT
    def get_depts(self):
        ret = []
        # cursor = connection을 이용해서 작업할 수 있는 기능을 생성
        curs = db_connection.get_db().cursor()
        
        # 쿼리 작성
        sql = 'select * from dept ;'
        curs.execute(sql)
        
        rows = curs.fetchall()
        # 결과를 딕셔너리 형태로 리스트에 저장
        for e in rows:
            temp = {'deptno':e[0], 'dname':e[1], 'loc':e[2]}
            ret.append(temp)
        
        db_connection.get_db().close()
        return ret
    
    # INSERT
    def insert_dept(self, deptno, dname, loc):
        curs = db_connection.get_db().cursor()
        
        sql = 'insert into dept (deptno, dname, loc) values(%s, %s, %s) ;'
        insert_num = curs.execute(sql,(deptno, dname, loc))
        
        # commit() -> autoCommit = True이기 때문에 따로 하지 않음
        
        db_connection.get_db().close()
       
	      # return f'insert OK : {insert_num}'
        return 'insert ok {0}'.format(insert_num)
    
    # UPDATE
    def update_dept(self, deptno, dname, loc):
        curs = db_connection.get_db().cursor()
        
        sql = 'update dept set dname=%s, loc=%s where deptno=%s ;'
        update_cnt = curs.execute(sql,(dname, loc, deptno))
        
        db_connection.get_db().close()
        return f'updete ok : {update_cnt}'
    
    # DELETE 
    def delete_dept(self, deptno):
        curs = db_connection.get_db().cursor()
        
        sql = 'delete from dept where deptno=%s ;'
        delete_cnt = curs.execute(sql, deptno)
        
        db_connection.get_db().close()
        
        return f'delete ok : {delete_cnt}'

        
if __name__ == '__main__':
    print(DeptDao().insert_dept(12, 'test1', 'loc1'))
    print(DeptDao().update_dept(12,'test111','loc111'))
    print(DeptDao().delete_dept(12))
    emplist = DeptDao().get_depts()
    print(emplist)
    