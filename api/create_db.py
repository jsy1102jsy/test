import pymysql

# MySQL 연결 설정
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='jsy1102!!',
    port=3306 #Mysql 포트 번호 (기본값: 3306)
)

try:
    with connection.cursor() as cursor:
        # 데이터베이스 생성
        cursor.execute("CREATE DATABASE IF NOT EXISTS matchball CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("데이터베이스 'matchball'이 성공적으로 생성되었습니다.")
        
    connection.commit()
    
except Exception as e:
    print(f"오류 발생: {e}")
    
finally:
    connection.close() 