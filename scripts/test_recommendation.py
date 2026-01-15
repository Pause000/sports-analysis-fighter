import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import recommend_service_logic, load_resources

def test_recommendations():
    print("Loading resources...")
    load_resources()
    
    test_queries = [
        ("K리그 팬덤 분위기, 강력한 전력, 전통의 명문, 유니폼이 예쁜 운영 스타일을 선호해요.", "kleague"),
        ("KBO 팬덤 분위기, 강력한 마운드, 오랜 역사, 젊고 역동적인 이미지 운영 스타일을 선호해요.", "kbo"),
        ("저는 리버풀 팬이고, 명문 구단 같은 팬덤 분위기 + 강력한 자본력 전력 + 오랜 역사 서사 + 유니폼이 예쁜 감성 + 강력한 자본력 운영 스타일을 선호해요.", "epl")
    ]
    
    for query, league in test_queries:
        print(f"\n--- Testing League: {league} ---")
        print(f"Query: {query}")
        result = recommend_service_logic(
            query=query,
            user_type=0,
            support_team=None,
            target_league=league
        )
        
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Recommended Team: {result['team_name']}")
            print(f"Match Percent: {result['match_percent']}%")
            print(f"League in result data: {result['team_data'].get('league')}")

if __name__ == "__main__":
    test_recommendations()
