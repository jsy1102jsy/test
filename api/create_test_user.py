import requests
import pymysql
import time

def register_users():
    url = "http://127.0.0.1:80/register"
    session = requests.Session()
    user_num = 1

    for team in ['a', 'b', 'c']:
        for i in range(1, 7):  # 리더 1 + 멤버 5 = 6명씩
            time.sleep(0.3)
            #team_a_1
            #team_a_1
            #pw1234
            name = f"team_{team}_{i}"
            email = f"{name}@test.com"
            form_data = {
                "email": email,
                "password": "pw1234",
                "passwordcheck": "pw1234",
                "name": name,
                "city": "Seoul"
            }
            r = session.post(url, data=form_data)
            print(f"[REGISTER] {email} → {r.status_code}")
            user_num += 1

def assign_teams():
    conn = pymysql.connect(host='localhost', user='root', password='jsy1102!!', db='matchball', charset='utf8')
    cur = conn.cursor()

    # 기존 데이터 정리
    cur.execute("DELETE FROM member")
    cur.execute("DELETE FROM team")

    # 팀 생성
    cur.execute("INSERT INTO team (name, level, city, people, detail, leader_id) VALUES ('team_a', 'Beginner', 1, 5, 'Team A detail', 1)")
    cur.execute("INSERT INTO team (name, level, city, people, detail, leader_id) VALUES ('team_b', 'Intermediate', 1, 5, 'Team B detail', 7)")
    cur.execute("INSERT INTO team (name, level, city, people, detail, leader_id) VALUES ('team_c', 'Expert', 1, 5, 'Team C detail', 13)")

    # 멤버 지정
    for uid in range(1, 7):
        cur.execute("INSERT INTO member (team_id, user_id) VALUES (1, %s)", (uid,))
    for uid in range(7, 13):
        cur.execute("INSERT INTO member (team_id, user_id) VALUES (2, %s)", (uid,))
    for uid in range(13, 19):
        cur.execute("INSERT INTO member (team_id, user_id) VALUES (3, %s)", (uid,))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ 기존 데이터 초기화 및 팀 생성 완료")


if __name__ == "__main__":
    #register_users()
    assign_teams()
