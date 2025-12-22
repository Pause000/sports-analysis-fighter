# =========================================================
# 🏆 [Project 1조] 범용 스포츠(EPL, K리그, KBO, F1) 성향 분석기
# =========================================================

import os
import time
import json
import google.generativeai as genai
from dotenv import load_dotenv
import os

# 1. API 설정
API_KEY = os.getenv('api_key')  # ⚠️ 본인의 API 키 입력
genai.configure(api_key=API_KEY)

# 최신 모델 사용
model_name = 'models/gemini-flash-latest' 
model = genai.GenerativeModel(model_name)

# 2. 데이터 로드 함수
def load_team_data(directory, file_names):
    merged_text = ''
    if not os.path.exists(directory):
        return ""
    folders_names = os.listdir(directory)
    for folder in folders_names:
        folder_path = os.path.join(directory, folder)
        if os.path.isdir(folder_path):
            for txt_name in file_names:
                txt_path = os.path.join(folder_path, txt_name)
                if os.path.isfile(txt_path):
                    try:
                        with open(txt_path, 'r', encoding='utf-8') as f:
                            merged_text += f.read() + '\n'
                    except:
                        pass
    return merged_text

# 3. [핵심] 범용 채점 로직이 적용된 분석 함수
def analyze_team_universal(team_name, text_data):
    if not text_data:
        print(f"❌ {team_name}: 데이터 없음")
        return None

    # 무료 티어 안정성을 위해 길이 제한
    input_text = text_data[:45000]
    
    print(f"▶ [{team_name}] 범용 기준(EPL/K리그/KBO/F1) 적용 중... ({len(input_text)}자)")

    # ⭐️ 4개 종목을 모두 포괄하는 프롬프트 설계
    prompt = f"""
    너는 스포츠 데이터 분석가야. 텍스트를 분석하여 '{team_name}'의 성향 데이터를 JSON으로 추출해.
    대상 종목은 [축구(EPL, K리그), 야구(KBO), 모터스포츠(F1)] 중 하나야.

    [필수 규칙]
    1. 오직 JSON 형식만 출력해. (마크다운 ```json 금지)
    2. 점수는 **0점부터 10점** 사이의 정수.
    3. 아래 **[범용 채점 기준]**을 종목에 맞게 해석해서 적용해.

    [범용 채점 기준 (0~10점)]

    1. **strength (전력/성적)**
       - (축구) 우승 경쟁권, 챔스 진출권이면 고득점.
       - (야구) 한국시리즈 우승, 가을야구(포스트시즌) 단골이면 고득점.
       - (F1)  컨스트럭터 상위권(레드불/페라리 등), 포디움 자주 오르면 고득점.

    2. **money (자본력/예산)**
       - (축구) '빅클럽', 이적료 지출 큼, 구단주가 부자(오일머니 등).
       - (야구) 모기업이 대기업(삼성, LG 등), FA 큰손, 연봉 총액 상위.
       - (F1)  막대한 차량 개발비, 팩토리 규모 큼, 메이저 제조사(Mercedes, Ferrari).

    3. **star_power (스타성)**
       - (공통) 누구나 아는 슈퍼스타 보유 (손흥민, 류현진, 루이스 해밀턴 등).
       - (공통) 팀 브랜드 자체가 유명하고 뉴스에 자주 나옴.

    4. **attack_style (경기 운영 스타일: 화끈함 vs 실리)**
       - **10점에 가까울수록 (공격/화끈함/리스크)**:
         * (축구) 닥공, 라인을 올림, 다득점 선호.
         * (야구) '빅볼', 거포 군단, 홈런 위주 타격전.
         * (F1)  공격적인 추월 시도, 과감한 전략, 리스크를 감수하는 드라이빙.
       - **0점에 가까울수록 (수비/실리/안정)**:
         * (축구) 선수비 후역습, 텐백, 짠물 수비.
         * (야구) '스몰볼', 투수 놀음, 작전 야구, 지키는 야구.
         * (F1)  타이어 관리 중심, 안정적 완주, 포인트 관리 위주.

    5. **underdog_feel (도전자/반란의 이미지)**
       - (공통) 약팀이 강팀을 잡는 이미지, '도깨비팀', 재정적 열세를 투지로 극복.
       - (0점은 압도적 1황, '공공의 적', 너무 강해서 재미없는 팀)

    6. **fan_passion (팬덤 화력)**
       - (축구/야구) 경기장 응원 소리가 큼, 원정 팬도 많음, 서포터즈 조직력.
       - (F1) '티포시(Tifosi)' 같은 열광적 팬덤, 굿즈 판매량, 글로벌 인기.

    7. **tradition (역사/헤리티지)**
       - (공통) 창단 연도가 오래됨, 과거 우승 트로피가 많음, '근본' 있는 팀.

    [출력 JSON 포맷]
    {{
      "league": "string (예: EPL, K League 1, KBO, F1)",
      "sport": "string (예: Football, Baseball, Motorsport)",
      "team_name": "{team_name}",
      "home_city": "string or null (F1은 본사 위치)",
      "home_stadium": "string or null (F1은 서킷 주행이므로 'Global' 또는 null)",
      "founded_year": number or null,
      "style_tags": ["태그1", "태그2", "태그3", ...],
      "scores": {{
        "strength": 0~10, 
        "money": 0~10,
        "star_power": 0~10,
        "attack_style": 0~10,
        "underdog_feel": 0~10,
        "fan_passion": 0~10,
        "tradition": 0~10
      }},
      "meta_description": "팀 설명(한 줄 요약)"
    }}

    [분석할 텍스트]
    {input_text}
    """

    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # 마크다운 제거
        if result_text.startswith("```"):
            result_text = result_text.replace("```json", "").replace("```", "").strip()
            
        data = json.loads(result_text)
        return data
    except Exception as e:
        print(f"⚠️ 에러 발생 ({team_name}): {e}")
        return None

# ---------------------------------------------------------
# 4. 실행부 (종목 섞어서 테스트 권장)
# ---------------------------------------------------------
base_dir = r"" # ⚠️ 경로 수정 필요

# 테스트용 팀 목록 (축구, 야구, F1 등 다양하게 넣어보세요)
teams = {
    # 축구
    # "🔵 첼시": ['첼시 FC.txt', 'Chelsea.txt', 'Chelsea FC.txt', '첼시_full.txt'],
    # 야구 (데이터가 있다면)
    # "🦁 삼성 라이온즈": ['삼성 라이온즈.txt'],
    # F1 (데이터가 있다면)
    # "🏎️ 페라리": ['Scuderia Ferrari.txt'], 
}

final_database = []

print("🚀 [통합] 전 종목 범용 분석 시작...\n")

for team_name, file_list in teams.items():
    text_data = load_team_data(base_dir, file_list)
    team_json = analyze_team_universal(team_name, text_data)
    
    if team_json:
        final_database.append(team_json)
        print(f"✅ 완료: {team_json.get('team_name')} ({team_json.get('sport')})")
        print(f"   📊 점수: {team_json.get('scores')}")
        print("-" * 50)
    
    time.sleep(5) 

# 저장
output_file = 'universal_team_scores.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(final_database, f, ensure_ascii=False, indent=2)

print(f"\n🎉 통합 분석 완료! '{output_file}' 저장됨.")