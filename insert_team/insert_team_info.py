import os
import json
from db.mysql import get_connection

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def insert_one_team(json_path, cursor):
    """JSON 1개 → team_info INSERT"""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

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

    cursor.execute(sql, (
        data["team_name"],
        data["league"],
        data["home_city"],
        data["home_stadium"],
        None,
        None
    ))


def insert_all_teams():
    conn = get_connection()
    cursor = conn.cursor()

    inserted = 0

    # data 폴더 아래 모든 하위 폴더 순회
    for folder_name in os.listdir(DATA_DIR):
        folder_path = os.path.join(DATA_DIR, folder_name)

        if not os.path.isdir(folder_path):
            continue

        print(f"\n📂 폴더 처리 시작: {folder_name}")

        # 각 폴더 안의 json 파일 처리
        for file_name in os.listdir(folder_path):
            if not file_name.endswith(".json"):
                continue

            json_path = os.path.join(folder_path, file_name)

            try:
                insert_one_team(json_path, cursor)
                inserted += 1
                print(f"  ✔ INSERT 성공: {file_name}")
            except Exception as e:
                print(f"  ❌ 실패: {file_name} → {e}")

    conn.commit()
    cursor.close()
    conn.close()

    print(f"\n🎉 전체 INSERT 완료 (총 {inserted}개)")


if __name__ == "__main__":
    insert_all_teams()
