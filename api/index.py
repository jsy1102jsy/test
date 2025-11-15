print("App is starting")
from flask import Flask, render_template, redirect, request, send_from_directory, session, jsonify
from flask_migrate import Migrate
import os
from api.models import db, User, Team, Board, JoinList, Member, Match
from api.utils.alarms import get_all_alarms_for_user
from api.utils.user import login, create_user
from api.utils.board import create_board
# api/index.py
# from flask import Flask
# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Hello Flask!"


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://jsy1102:Jsy1102!^@13.125.208.147:3306/matchball'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'adnofnadoifn243AB'
UPLOAD_FOLDER = "/tmp/files"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# 데이터베이스 초기화
db.init_app(app)
migrate = Migrate(app, db)

# files 폴더가 없으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# MySQL에서는 외래키 제약조건이 자동으로 활성화되므로 별도 설정 불필요


CITY_MAP = {
    '서울': 1,
    '부산': 2,
    '대구': 3,
    '인천': 4,
    '광주': 5,
    '대전': 6,
    '울산': 7,
    '세종': 8,
    '경기': 9,
    '강원': 10,
    '충북': 11,
    '충남': 12,
    '전북': 13,
    '전남': 14,
    '경북': 15,
    '경남': 16,
    '제주': 17
}
CITY_REVERSE_MAP = {v: k for k, v in CITY_MAP.items()}

def get_current_user(): #현재 로그인되어있으면 True, 그렇지않으면 False를 반환하는 함수
    if 'username' in session :
        email = session['username']
        user = User.query.filter_by(email = email).first()
        return user if user else None#만약 유저가 있으면 유저를 리턴하고 그렇지 않으면 login으로 간다
    else:
        return None
    

@app.route('/',methods=['GET'])
def head():
    # 필터 파라미터 가져오기
    region_filter = request.args.get('region', '')
    date_filter = request.args.get('date', '')
    sort_filter = request.args.get('sort', 'latest')
    
    # 기본 쿼리
    query = Board.query
    
    # 지역 필터 적용
    if region_filter:
        query = query.filter(Board.city == region_filter)
    
    # 날짜 필터 적용
    if date_filter:
        from datetime import datetime, timedelta
        today = datetime.now().date()
        
        if date_filter == 'today':
            today_str = today.strftime('%Y-%m-%d')
            query = query.filter(Board.date == today_str)
        elif date_filter == 'week':
            week_ago = today - timedelta(days=7)
            week_ago_str = week_ago.strftime('%Y-%m-%d')
            query = query.filter(Board.date >= week_ago_str)
        elif date_filter == 'month':
            month_ago = today - timedelta(days=30)
            month_ago_str = month_ago.strftime('%Y-%m-%d')
            query = query.filter(Board.date >= month_ago_str)
        elif date_filter == '3months':
            three_months_ago = today - timedelta(days=90)
            three_months_ago_str = three_months_ago.strftime('%Y-%m-%d')
            query = query.filter(Board.date >= three_months_ago_str)
    
    # 정렬 적용
    if sort_filter == 'latest':
        query = query.order_by(Board.id.desc())
    elif sort_filter == 'oldest':
        query = query.order_by(Board.id.asc())
    elif sort_filter == 'title':
        query = query.order_by(Board.title.asc())
    
    posts = query.all()
    
    # 작성자 이름 가져오기
    names = []
    for post in posts:
        user = User.query.filter_by(id=post.user_id).first()
        names.append(user.name if user else '알 수 없음')
    user = get_current_user()
    print(user)
    if user:
        print("LOGIN !!")
        return render_template('index.html', posts=posts, isLogin = True, names = names, 
                            region_filter=region_filter, date_filter=date_filter, sort_filter=sort_filter) 
    else:
        print("no login ")
        return render_template('index.html', posts = posts, isLogin = False, names=names,
                             region_filter=region_filter, date_filter=date_filter, sort_filter=sort_filter)

@app.route('/alarm')
def alarm():
    if 'username' not in session:
        return redirect('/login')
    user = User.query.filter_by(email=session['username']).first()
    if not user:
        return redirect('/login')
    # 팀 리더가 속한 팀 찾기
    alarms = get_all_alarms_for_user(user)
    
    return render_template('alarm.html', isLogin=True, alarms=alarms)

@app.route('/login',methods=['POST','GET'])
def get_form():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['pwname']                                                                                                                                       
        isLogin, msg = login(email, pwd)
        if isLogin:
            return redirect('/')
        else:
            return render_template('login.html', msg=msg, isLogin=False)
    else:
        return render_template('login.html', isLogin=False)

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['password']
        pw2 = request.form['passwordcheck']
        name = request.form['name']
        city = request.form['city']
        islogin,msg = create_user(email = email, pw = pw, pw2 = pw2, name = name, city = city)
        if islogin:
            return redirect('/login')
        else:
            return render_template('register.html', msg=msg, isLogin= False)

       
    return render_template('register.html', isLogin= False)

@app.route('/board', methods=['GET', 'POST'])
def board():
    user = get_current_user()
    if user: #로그인 되어있을 때... 
        if request.method == 'POST':
            date = request.form['date']
            time = request.form['time']
            level = request.form['level']
            title = request.form['title']
            detail = request.form['detail']
            city = request.form['city']
            lat = request.form['lat']
            lng = request.form['lng']

            if (not lat):
                lat = "38"
                lng = "38"
            result, msg = create_board(user, date, time, level, title, detail, city, lat, lng)
            if result:
                return redirect("/")
            else:
                return render_template('post.html', msg=msg, isLogin=True)
        else: return render_template('post.html', isLogin = True)
    else:
        return redirect('/login')

@app.route('/getTeamList/<int:num>', methods=['GET'])
def getTeamDetail(num):
    now_user = get_current_user()
    if not isinstance(now_user, User):
        return redirect('/login')  # None 대신 반드시 Response 객체 반환
 # redirect('/login')

    team = Team.query.filter_by(id=num).first()
    if not team:
        return redirect('/')

    members = Member.query.filter_by(team_id=num).all()
    users = [User.query.filter_by(id=m.user_id).first() for m in members]

    team_leader = User.query.filter_by(id=team.leader_id).first()
    users.append(team_leader)

    team.city_display = CITY_REVERSE_MAP.get(team.city, '미입력')
    is_leader = now_user.id == team_leader.id

    return render_template(
        'teamshow.html',
        team=team,
        isLogin=True,
        users=users,
        team_leader=team_leader,
        is_leader=is_leader
    )


@app.route('/getPostList/<int:num>', methods=['GET'])
def getPostDetail(num):
    current_user = get_current_user()
    if not current_user:
        return redirect('/login')   # 🔒 로그인 안 한 경우 로그인 페이지로 이동

    post = Board.query.filter_by(id=num).first()
    if not post:
        return "게시글을 찾을 수 없습니다.", 404

    uid = post.user_id
    user = User.query.filter_by(id=uid).first()
    member = Member.query.filter_by(user_id=uid).first()
    teamname = "팀 없음"
    if member:
        team = Team.query.filter_by(id=member.team_id).first()
        teamname = team.name if team else "팀 없음"

    return render_template(
        'postshow.html',
        post=post,
        isLogin=True,
        name=user.name if user else "알 수 없음",
        current_user_id=current_user.id,
        teamname=teamname
    )


@app.route('/deletePost/<int:num>', methods=['DELETE'])
def deletePost(num):
    if not session.get('username'):
        return jsonify({'success': False, 'message': '로그인이 필요합니다.'}), 401
    post = Board.query.filter_by(id=num).first()
    if not post:
        return jsonify({'success': False, 'message': '게시글을 찾을 수 없습니다.'}), 404
    current_user = get_current_user()
    if not current_user or post.user_id != current_user.id:
        return jsonify({'success': False, 'message': '권한이 없습니다.'}), 403
    db.session.delete(post)
    db.session.commit()
    return jsonify({'success': True, 'message': '게시글이 삭제되었습니다.'}), 200

@app.route('/editPost/<int:num>', methods=['GET', 'POST'])
def editPost(num):
    if not session.get('username'):
        return redirect('/login')
    post = Board.query.filter_by(id=num).first()
    if not post:
        return redirect('/')
    # 현재 로그인한 사용자가 글의 작성자인지 확인
    email = session['username']
    current_user = User.query.filter_by(email=email).first()
    if not current_user or post.user_id != current_user.id:
        return redirect('/')
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.date = request.form['date']
        post.time = request.form['time']
        post.level = request.form['level']
        post.city = request.form['city']
        post.detail = request.form['detail']
        
        db.session.commit()
        return redirect(f'/getPostList/{post.id}')
    
    return render_template('postreform.html', post=post, isLogin=True)

@app.route("/teamlist", methods=['GET'])
def teamlist():
    teams = Team.query.all()
    for team in teams:
        team.city_display = CITY_REVERSE_MAP.get(team.city, '미입력')
    isLogin = False
    current_user_team = None
    print("register")
    if 'username' in session :
        print("username in session")
        isLogin = True
        email = session['username']
        user = User.query.filter_by(email = email).first()
        if user:
            current_user_team = Team.query.filter_by(leader_id=user.id).first()
            if current_user_team:
                current_user_team.city_display = CITY_REVERSE_MAP.get(current_user_team.city, '미입력')
    
    isLeader = False
    if current_user_team:
        isLeader = True
    
    return render_template('teamlist.html', teams = teams, current_user_team = current_user_team, isLogin = isLogin, isLeader = isLeader)

@app.route('/team', methods=['POST', 'GET'])
def team():
    user = get_current_user()
    if not isinstance(user, User):
        return user  # redirect('/login') 반환됨

    if user:
        if request.method == 'POST':
            if 'file' not in request.files:
                return 'No file part'
            team_name = request.form['teamname']
            team_level = request.form['level']
            city = request.form['city']
            people = int(request.form['people'])
            detail = request.form['detail']
            file = request.files['file']
            
            # 파일 이름만 가져오기
            filename = file.filename
            # 파일을 저장할 경로
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            print("팀을 생성 이름: " + team_name)
            print("팀을 생성하는 레벨: " + team_level)
            print("팀을 생성하는 지역: " + city)
            print("팀 인원수: ", people)
            print("팀 소개: " + detail)
            print("팀 로고: " + filename)  # filename만 출력
            
            # 팀 객체를 생성할 때 filename만 저장
            city_code = CITY_MAP.get(city, 1)  # Default to Seoul (1) if city not found
            team = Team(
                name=team_name,
                level=team_level,
                city=city_code,
                people=people,
                detail=detail,
                file_name=filename,  # file_path 대신 filename 사용
                leader_id=user.id
            )
            member = Member(team=team, user=user)
            
            db.session.add(team)
            db.session.add(member)
            db.session.commit()
            return render_template('index.html' , isLogin = True)

            
        return render_template('team.html' , isLogin = True)

@app.route('/files/<filename>')
def files(filename):
    print("CHECK")
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/match-request", methods=['GET', 'POST'])
def match_request():
    if 'username' not in session:
        return redirect('/login')

    user = User.query.filter_by(email=session['username']).first()
    if not user:
        return redirect('/login')

    # 사용자가 속한 팀 확인
    # 리더팀 또는 멤버팀 중 하나라도 존재하면 user_team에 저장
    user_team = Team.query.filter_by(leader_id=user.id).first()
    if not user_team:
        membership = Member.query.filter_by(user_id=user.id).first()
        if membership:
            user_team = Team.query.get(membership.team_id)

    if request.method == 'GET':
        teamName = request.args.get('teamName')
        return render_template(
            'match.html',
            teamName=teamName,
            isLogin=True,
            user_team=user_team  # 팀이 있으면 True, 없으면 None
        )

    else:  # POST 요청
        if not user_team:
            return jsonify({"status": "error", "MSG": "팀이 없어 경기 신청이 불가능합니다."}), 403

        data = request.get_json()
        details = data.get('details')
        teamName = data.get('teamName')

        team = Team.query.filter_by(name=teamName).first()
        if not team:
            return jsonify({"status": "error", "MSG": "상대 팀을 찾을 수 없습니다."}), 404

        # 경기 신청 저장
        match = Match(
            team_id=team.id,
            user_id=user.id,
            details=details,
        )
        db.session.add(match)
        db.session.commit()
 
        return jsonify({"status": "success", "MSG": "경기 신청 완료"}), 200
   
@app.route('/matchlist', methods=['GET'])
def matchlist():
    if 'username' not in session:
        return redirect('/login')
    user = User.query.filter_by(email=session['username']).first()
    if not user:
        return redirect('/login')

    matches = Match.query.all()
    match_data = []
    for match in matches:
        team = Team.query.filter_by(id=match.team_id).first()
        if team and match.user_id == user.id:
            match_data.append({
                'id': match.id,
                'details': match.details,
                'team_name': team.name
            })

    return render_template('matchlist.html', matches=match_data, isLogin=True)


@app.route('/mypage')
def mypage():
    isLogin = False  
    user = None
    if not session.get('username'):
        return redirect('/login')
    email = session['username']
    user = User.query.filter_by(email=email).first() 
    if user:
        isLogin = True
        # 사용자가 작성한 게시글 가져오기
        my_posts = Board.query.filter_by(user_id=user.id).order_by(Board.created_at.desc()).all()
        # 사용자가 속한 팀 정보 가져오기
        my_team = Team.query.filter_by(leader_id=user.id).first()
        if my_team:
            my_team.city_display = CITY_REVERSE_MAP.get(my_team.city, '미입력')
    else:
        return redirect('/login')  

    return render_template('mypage.html', user=user, my_posts=my_posts, my_team=my_team, isLogin=True)

@app.route('/myposts')
def myposts():
    if not session.get('username'):
        return redirect('/login')
    
    email = session['username']
    user = User.query.filter_by(email=email).first()
    if not user:
        return redirect('/login')
    
    # 사용자가 작성한 게시글 가져오기
    my_posts = Board.query.filter_by(user_id=user.id).order_by(Board.created_at.desc()).all()
    
    return render_template('myposts.html', user=user, my_posts=my_posts, isLogin=True)

@app.route('/logout')
def logout():
    session.clear()  # 세션 전체 제거
    return redirect('/')

@app.route('/leave', methods=['POST'])
def leave_service():
    email = session.get('username')
    if not email:
        return jsonify({'success': False, 'message': '로그인이 필요합니다.'}), 401
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'success': False, 'message': '사용자를 찾을 수 없습니다.'}), 404
    db.session.delete(user)
    db.session.commit()
    session.pop('username', None)
    return jsonify({'success': True, 'message': '회원 탈퇴가 완료되었습니다.'}), 200
        
@app.route("/join-team", methods=['POST','GET'])
def join_team():
    if request.method == 'GET':
        teamName = request.args.get('teamName')
        isLogin = 'username' in session
        userId = None
        if isLogin:
            user = User.query.filter_by(email=session['username']).first()
            if user:
                userId = user.id
        return render_template('teamsignup.html', teamName=teamName, isLogin=isLogin, userId=userId)
    elif request.method == 'POST':
        data = request.get_json()
        details = data.get('details')
        teamName = data.get('teamName')
        teamId = Team.query.filter_by(name=teamName).first().id
        if 'username' in session :
            userId = User.query.filter_by(email = session['username']).first().id
            print("userId: ", userId)
            print("teamId: ", teamId)
            isLogin = True
            email = session['username']
            newteam = JoinList(email = email,details = details, team_id = teamId, user_id = userId) #여기 수정
            db.session.add(newteam)
            db.session.commit()
            return jsonify({
                    "status": "success",
                    "MSG": "가입 성공"
                }), 200
        
@app.route("/userdetails", methods=["GET"]) #가입 신청 목록 확인.
def user_details():
    if 'username' in session : #로그인 되어 있을 때
        print("성공적으로 로그인 되어 있습니다.")
        isLogin = True
        email = session['username']
        user = User.query.filter_by(email = email).first()
        team = Team.query.filter_by(leader_id = user.id).first()
        if team: 
            joinlist = JoinList.query.filter_by(team_id=team.id)
            print(joinlist)
    else :
        return redirect('/login')
    return render_template("userdetails.html", joinlist=joinlist ,isLogin = isLogin)

@app.route("/handle-decision", methods=["POST"])
def handle_request():
    current_user = get_current_user()  # 오타 수정
    if not isinstance(current_user, User):
        return current_user  # redirect 처리

    data = request.get_json()
    request_id = data.get('id')
    alarm_type = data.get('type')
    action = data.get('action')

    if alarm_type == 'match':
        match_info = Match.query.filter_by(id=request_id).first()
        if not match_info:
            return jsonify({"status": "error", "MSG": "경기 신청을 찾을 수 없습니다."}), 404

        db.session.delete(match_info)
        db.session.commit()
        msg = "경기 신청 승인 완료" if action == 'approve' else "경기 신청 거절 완료"
        return jsonify({"status": "success", "MSG": msg}), 200

    elif alarm_type == 'join':
        join_info = JoinList.query.filter_by(id=request_id).first()
        if not join_info:
            return jsonify({"status": "error", "MSG": "가입 신청을 찾을 수 없습니다."}), 404

        team = Team.query.filter_by(leader_id=current_user.id).first()
        if not team:
            return redirect("/")

        if action == 'approve':
            member = Member(user_id=join_info.user_id, team_id=team.id)
            db.session.add(member)
            db.session.delete(join_info)
            db.session.commit()
            return jsonify({"status": "success", "MSG": "가입 승인 완료"}), 200
        else:
            db.session.delete(join_info)
            db.session.commit()
            return jsonify({"status": "success", "MSG": "가입 거절 완료"}), 200

    return jsonify({"status": "error", "MSG": "요청 유형이 잘못되었습니다."}), 400


# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True, host='0.0.0.0', port=80)    



# render_template 할 때 lat랑 lng변수로 전달해서 사용자가 입력한 값의 위, 경도로 지도를 띄우기