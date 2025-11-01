from models import User, Team, JoinList, Match
def get_created_at(alarm):
    return alarm["created_at"]

def get_all_alarms_for_user(user: User):
    team = Team.query.filter_by(leader_id=user.id).first()
    alarms = []
    if team:
        # 팀 가입 신청 목록 (최신순)
        joinlist = JoinList.query.filter_by(team_id=team.id).order_by(JoinList.id.desc()).all()
        for req in joinlist:
            alarms.append({
                "type": "join",
                "created_at": req.created_at,  # id 대신 created_at을 넣는다.
                "email": req.email,
                "details": req.details,
                "id": req.id
            })
        # 경기 신청 목록 (최신순)
        matchlist = Match.query.filter_by(team_id=team.id).order_by(Match.id.desc()).all()
        for match in matchlist:
            user_name = User.query.filter_by(id=match.user_id).first().name if match.user_id else "알 수 없음"
            alarms.append({
                "type": "match",
                "created_at": match.created_at if hasattr(match, "created_at") else match.id,
                "user_name": user_name,
                "details": match.details,
                "id": match.id
            })
        alarms.sort(key=get_created_at, reverse=True)
        return alarms