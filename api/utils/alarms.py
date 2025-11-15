from api.models import User, Team, JoinList, Match
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
                "created_at": req.created_at,
                "email": req.email,
                "details": req.details,
                "id": req.id
            })
        matchlist = Match.query.filter_by(opponent_team_id=team.id).order_by(Match.id.desc()).all()
        for match in matchlist:
            request_team_name = Team.query.get(match.request_team_id).name if match.opponent_team_id else "알 수 없음"
            alarms.append({
                "type": "match",
                "created_at": match.created_at,
                "request_team_name": request_team_name,
                "details": match.details,
                "id": match.id,
                "isEnd": match.isEnd
            })

        # 생성일 기준 정렬
        alarms.sort(key=get_created_at, reverse=True)

    return alarms
