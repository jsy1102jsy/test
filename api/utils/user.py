from flask import session
from werkzeug.security import check_password_hash ,generate_password_hash
from api.models import User, db

def login(email, pwd):
    user = User.query.filter_by(email=email).first() #뭐하는건지..달아..
    if user is None:
        return False, "해당하는 유저가 존재하지 않습니다."
    if user and check_password_hash(user.password, pwd):
        session['username'] = email  #로그인한 사용자 이메일을 세션에 저장(로그인 상태 유지)
        return True, None
    else:
        return False, "비밀번호가 일치하지 않습니다."


def create_user(email,pw,pw2,name,city):
    user=User.query.filter_by(email=email).first()   #이미 가입된 이메일인지 확인
    hashed_password=generate_password_hash(pw)
    if user:   #중복 회원이면 실패
        return False,"이미 가입 된 아이디 입니다."
    if len(pw)<4:  #비밀번호 길이 체크
        return False,"비밀번호 길이는 4자리 이상 입니다."
    if pw!=pw2:   #비밀번호 확인 불일치
        return False,"비밀번호가 틀립니다."
    else:
        print("회원가입 확인 성공!")
        newuser=User(password=hashed_password,name=name,email=email,city=city)  #새 유저 객체
        db.session.add(newuser)  #DB에 추가
        db.session.commit()#커밋(저장)
        print("회원가입 성공, 데이터베이스 저장 완료")
        return True,None