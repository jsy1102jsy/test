import requests
import pymysql
import time

def register_users():
    url = "https://test-ten-henna.vercel.app/register"
    session = requests.Session()
    user_num = 1

    for team in ['a', 'b', 'c']:
        for i in range(1,4):  # 리더 1 + 멤버 5 = 6명씩
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
    conn = pymysql.connect(host='13.125.208.147', user='jsy1102', password='Jsy1102!^', db='matchball', charset='utf8')
    cur = conn.cursor()

    # 기존 데이터 정리
    cur.execute("DELETE FROM member")
    cur.execute("DELETE FROM team")

    # 팀 생성
    cur.execute("INSERT INTO team (name, level, city, people, detail, leader_id) VALUES ('team_a', 'Beginner', 1, 5, 'Team A detail', 1)")
    cur.execute("INSERT INTO team (name, level, city, people, detail, leader_id) VALUES ('team_b', 'Intermediate', 1, 5, 'Team B detail', 4)")
    cur.execute("INSERT INTO team (name, level, city, people, detail, leader_id) VALUES ('team_c', 'Expert', 1, 5, 'Team C detail', 7)")

    # 멤버 지정
    for uid in range(1, 4):
        cur.execute("INSERT INTO member (team_id, user_id) VALUES (1, %s)", (uid,))
    for uid in range(4, 7):
        cur.execute("INSERT INTO member (team_id, user_id) VALUES (2, %s)", (uid,))
    for uid in range(7, 10):
        cur.execute("INSERT INTO member (team_id, user_id) VALUES (3, %s)", (uid,))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ 기존 데이터 초기화 및 팀 생성 완료")


if __name__ == "__main__":
    register_users()
    assign_teams()
