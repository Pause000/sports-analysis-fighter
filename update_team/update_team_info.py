# 현재 노트북 엔진에 직접 설치!
# import sys
# !{sys.executable} -m pip install pymysql cryptography

import os
import json
from db.mysql import get_connection

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def update_one_team(json_path, cursor):
    """JSON 1개 → team_info INSERT"""
    with open(json_path, "r", encoding="utf-8") as f:   # JSON 파일 열기
        data = json.load(f)

    # DB에 넣기 전에 JSON 타입이 필요한 데이터만 문자열로 미리 변환
    # 아래 execute 함수에서는 data["key"] 형태를 그대로 쓸 수 있음
    data["style_tags"] = json.dumps(data.get("style_tags", []), ensure_ascii=False)
    data["scores"] = json.dumps(data.get("scores", {}), ensure_ascii=False)

    sql = """
    UPDATE team_info 
    SET
        sport=%s,
        logo_url=%s,
        style_tags=%s,
        scores=%s,
        meta_description=%s
    WHERE team_name = %s
    """

    cursor.execute(sql, (
        data.get("sport"),
        data.get("logo_url"),
        data.get("style_tags"),      # 이미 위에서 변환했으므로 그대로 사용 가능
        data.get("scores"),          # 이미 위에서 변환했으므로 그대로 사용 가능
        data.get("meta_description"),
        data.get("team_name")
    ))

def update_all_teams():
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
                update_one_team(json_path, cursor)
                inserted += 1
                print(f"  ✔ INSERT 성공: {file_name}")
            except Exception as e:
                print(f"  ❌ 실패: {file_name} → {e}")

    conn.commit()
    cursor.close()
    conn.close()

    print(f"\n🎉 전체 INSERT 완료 (총 {inserted}개)")


if __name__ == "__main__":
    update_all_teams()