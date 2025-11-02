from app import app, db
from api.models import User, Team, Board, JoinList

with app.app_context():
    # 모든 테이블 생성
    db.create_all()
    print("모든 테이블이 성공적으로 생성되었습니다!")
    
    # 생성된 테이블 확인
    print("\n생성된 테이블:")
    for table in db.metadata.tables:
        print(f"- {table}") 