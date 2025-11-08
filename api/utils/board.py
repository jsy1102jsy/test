from models import User
from models import db, Board

def create_board(user, date, time, level, title, detail, city, lat, lng):
    if len(title) < 7:
        return False, "제목 길이는 7자리 이상 입니다."
    new_board = Board(
        date=date,
        time=time,
        level=level,
        title=title,
        detail=detail,
        city=city,
        lat=lat,
        lng=lng,
        user_id=user.id
    )
    db.session.add(new_board)
    db.session.commit()
    return True, "게시글이 성공적으로 작성되었습니다."