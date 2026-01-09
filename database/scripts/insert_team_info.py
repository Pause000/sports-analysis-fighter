# 운영체제(OS) 관련 기능을 쓰기 위한 라이브러리
# → 파일 경로 만들기, 현재 파일 위치 찾기 등에 사용
import os

# JSON 파일을 파이썬 딕셔너리로 읽기 위한 라이브러리
import json

# MySQL DB에 연결하는 함수 (직접 만든 모듈)
from db.mysql import get_connection


# 현재 이 파이썬 파일의 "절대 경로"를 가져옴
# 예: C:/project/insert_team.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# BASE_DIR 아래에 있는 data 폴더 경로 생성
# 예: C:/project/data
DATA_DIR = os.path.join(BASE_DIR, "data")


def insert_one_team(json_path, cursor):
    """
    JSON 파일 1개를 읽어서
    team_info 테이블에 INSERT 하는 함수
    """

    # json_path 위치에 있는 JSON 파일을 읽기 모드("r")로 열기
    # encoding="utf-8" → 한글 깨짐 방지
    with open(json_path, "r", encoding="utf-8") as f:
        # JSON → 파이썬 dict 형태로 변환
        data = json.load(f)

    # MySQL에 보낼 INSERT 쿼리
    # %s 는 나중에 값이 들어갈 자리 표시자
    sql = """
    INSERT INTO team_info (
        team_name,
        league,
        home_city,
        stadium,
        logo_url,
        main_color
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    # SQL 실행
    # data 딕셔너리에서 값을 꺼내서 순서대로 넣음
    cursor.execute(sql, (
        data["team_name"],        # 팀 이름
        data["league"],           # 리그 이름
        data["home_city"],        # 연고지
        data["home_stadium"],     # 홈 경기장
        None,                     # 로고 URL (아직 없어서 None)
        None                      # 메인 컬러 (아직 없어서 None)
    ))


def insert_all_teams():
    """
    data 폴더 아래의 모든 JSON 파일을 찾아서
    팀 정보를 전부 DB에 넣는 함수
    """

    # DB 연결
    conn = get_connection()

    # SQL 실행을 담당하는 커서 생성
    cursor = conn.cursor()

    # 몇 개의 팀이 INSERT 되었는지 세기 위한 변수
    inserted = 0

    # data 폴더 안에 있는 모든 파일/폴더 이름 가져오기
    for folder_name in os.listdir(DATA_DIR):

        # 폴더 이름을 절대 경로로 변환
        folder_path = os.path.join(DATA_DIR, folder_name)

        # 폴더가 아니면 (파일이면) 건너뜀
        if not os.path.isdir(folder_path):
            continue

        print(f"\n📂 폴더 처리 시작: {folder_name}")

        # 해당 폴더 안에 있는 파일들 하나씩 처리
        for file_name in os.listdir(folder_path):

            # 확장자가 .json이 아니면 무시
            if not file_name.endswith(".json"):
                continue

            # JSON 파일 전체 경로 생성
            json_path = os.path.join(folder_path, file_name)

            try:
                # JSON 하나 → DB INSERT
                insert_one_team(json_path, cursor)

                # 성공했으면 카운트 증가
                inserted += 1
                print(f"  ✔ INSERT 성공: {file_name}")

            except Exception as e:
                # 에러 발생 시 어떤 파일이 실패했는지 출력
                print(f"  ❌ 실패: {file_name} → {e}")

    # 지금까지 실행한 INSERT들을 실제 DB에 반영
    conn.commit()

    # 자원 정리 (매우 중요)
    cursor.close()
    conn.close()

    print(f"\n🎉 전체 INSERT 완료 (총 {inserted}개)")


# 이 파일을 직접 실행했을 때만 실행되는 코드
# 다른 파일에서 import하면 실행되지 않음
if __name__ == "__main__":
    insert_all_teams()
