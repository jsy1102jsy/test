import pymysql

# MySQL 연결
conn = pymysql.connect(
    host='13.125.208.147',
    user='jsy1102',
    password='Jsy1102!^',
    database='matchball',
    charset='utf8mb4',
    autocommit=True
)
cur = conn.cursor()

# 테이블 생성 쿼리
queries = [

    # User 테이블
    """
    CREATE TABLE IF NOT EXISTS user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        password VARCHAR(300) NOT NULL,
        name VARCHAR(30) NOT NULL,
        email VARCHAR(30) NOT NULL,
        city VARCHAR(30) NOT NULL
    )
    """,

    # Team 테이블
    """
    CREATE TABLE IF NOT EXISTS team (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(30) NOT NULL,
        level VARCHAR(20) NOT NULL,
        city INT NOT NULL,
        people INT NOT NULL,
        detail VARCHAR(300),
        file_name VARCHAR(100),
        leader_id INT UNIQUE NOT NULL,
        FOREIGN KEY (leader_id) REFERENCES user(id) ON DELETE CASCADE
    )
    """,

    # Board 테이블
    """
    CREATE TABLE IF NOT EXISTS board (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date VARCHAR(15) NOT NULL,
        time VARCHAR(15) NOT NULL,
        level VARCHAR(15) NOT NULL,
        title VARCHAR(100) NOT NULL,
        detail VARCHAR(300) NOT NULL,
        city VARCHAR(30) NOT NULL,
        user_id INT NOT NULL,
        lat FLOAT,
        lng FLOAT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
    )
    """,

    # JoinList 테이블
    """
    CREATE TABLE IF NOT EXISTS joinlist (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(30) NOT NULL,
        details VARCHAR(300) NOT NULL,
        team_id INT NOT NULL,
        user_id INT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (team_id) REFERENCES team(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
    )
    """,

    # Member 테이블
    """
    CREATE TABLE IF NOT EXISTS member (
        id INT AUTO_INCREMENT PRIMARY KEY,
        team_id INT,
        user_id INT,
        FOREIGN KEY (team_id) REFERENCES team(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
    )
    """,

    # Match 테이블
    """
    CREATE TABLE IF NOT EXISTS `match` (
        id INT AUTO_INCREMENT PRIMARY KEY,
        request_team_id INT NOT NULL,
        opponent_team_id INT NOT NULL,
        request_team_score INT DEFAULT 0,
        opponent_team_score INT DEFAULT 0,
        details VARCHAR(500),
        isEnd BOOLEAN DEFAULT FALSE,
        match_datetime DATETIME NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_accept BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (request_team_id) REFERENCES team(id) ON DELETE CASCADE,
        FOREIGN KEY (opponent_team_id) REFERENCES team(id) ON DELETE CASCADE
    );

    """,
    
    """
        CREATE TABLE IF NOT EXISTS joinlist (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(30) NOT NULL,
        details VARCHAR(300) NOT NULL,
        team_id INT NOT NULL,
        user_id INT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (team_id) REFERENCES team(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
    );
    """
]

# 쿼리 실행
for q in queries:
    cur.execute(q)
    print("테이블 생성 완료 혹은 이미 존재함.")

cur.close()
conn.close()
