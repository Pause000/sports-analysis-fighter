import os
import json
import time
import google.generativeai as genai

# 1. API 설정
# 1. API 설정
try:
    from dotenv import load_dotenv
    load_dotenv() # .env 파일 로드
except ImportError:
    print("⚠️ python-dotenv가 설치되지 않았습니다. .env 로드 실패 가능성 있음.")

API_KEY = os.getenv('api_key')  # ⚠️ .env의 변수명(api_key) 확인 완료

if not API_KEY:
    print("❌ Fatal Error: API Key is missing!")
    print("   Please check your .env file and ensure variable 'api_key' exists.")
    exit()

genai.configure(api_key=API_KEY)


model_name = 'models/gemini-flash-latest'
model = genai.GenerativeModel(model_name)

# ----------------------------
# 2. Gemini 분석 함수 (기존 프롬프트 유지)
# ----------------------------
def analyze_team(team_name, text_data):
    if not text_data: return None
    
    text_data = text_data[:30000]
    
    prompt = f"""
    너는 스포츠 데이터 분석가야. 텍스트를 분석하여 '{team_name}'의 성향 데이터를 JSON으로 추출해.
    대상 종목은 [축구(EPL, K리그), 야구(KBO), 모터스포츠(F1)] 중 하나야.

    [필수 규칙]
    1. 오직 JSON 형식만 출력해. (마크다운 ```json 금지)
    2. 점수는 **0점부터 10점** 사이의 정수.
    3. 아래 **[범용 채점 기준]**을 종목에 맞게 해석해서 적용해.

    [범용 채점 기준 (0~10점)]
    1. **strength (전력/성적)**
    2. **money (자본력/예산)**
    3. **star_power (스타성)**
    4. **attack_style (경기 운영 스타일: 화끈함 vs 실리)**
    5. **underdog_feel (도전자/반란의 이미지)**
    6. **fan_passion (팬덤 화력)**
    7. **tradition (역사/헤리티지)**

    [출력 JSON 포맷]
    {{
      "league": "string",
      "sport": "string",
      "team_name": "{team_name}",
      "home_city": "string or null",
      "home_stadium": "string or null",
      "founded_year": number or null,
      "style_tags": ["태그1", "태그2", "태그3"],
      "scores": {{
        "strength": 0~10, 
        "money": 0~10,
        "star_power": 0~10,
        "attack_style": 0~10,
        "underdog_feel": 0~10,
        "fan_passion": 0~10,
        "tradition": 0~10
      }},
      "meta_description": "팀 설명"
    }}

    [분석할 텍스트]
    {text_data}
    """

    try:
        response = model.generate_content(prompt)
        res = response.text.strip()
        # JSON 파싱을 위한 전처리
        if "```json" in res: res = res.split("```json")[1].split("```")[0].strip()
        return json.loads(res)
    except Exception as e:
        print(f"   ⚠️ '{team_name}' 분석 중 오류 발생: {e}")
        return None

# ----------------------------
# 3. 메인 실행부 (파일 로드 및 저장)
# ----------------------------
if __name__ == "__main__":
    # 데이터가 저장된 '스포츠이름' 폴더 경로로 수정하세요
    source_dir = r"C:\Python\project\KBO_text_data\헣전처리번역" 
    db = []

    if not os.path.exists(source_dir):
        print(f"❌ 경로를 찾을 수 없습니다: {source_dir}")
    else:
        files = [f for f in os.listdir(source_dir) if f.endswith('.txt')]
        print(f"🚀 총 {len(files)}개 팀 데이터 분석 시작")

        for file_name in files:
            team_name = file_name.replace('.txt', '').replace('_merge', '')
            file_path = os.path.join(source_dir, file_name)
            
            print(f"\n[분석 중] {team_name}...")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Gemini 분석 호출
            result = analyze_team(team_name, content)
            
            if result:
                db.append(result)
                print(f"✅ {team_name} 분석 완료")
            
            # API 할당량(Rate Limit)을 위해 5초간 대기 
            time.sleep(5)

        # 최종 결과 저장
        output_path = 'final_team_data.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        
        print("\n" + "="*50)
        print(f"✅ 전체 분석 완료. 저장된 파일: {output_path}")
        print("="*50)