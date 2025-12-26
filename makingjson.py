import os
import json
import time
import google.generativeai as genai

# 1. API 설정
try:
    from dotenv import load_dotenv
    load_dotenv() # .env 파일 로드
except ImportError:
    print("python-dotenv가 설치되지 않았습니다. .env 로드 실패 가능성 있음.")

API_KEY = os.getenv('api_key')  # .env의 변수명(api_key) 확인 완료

if not API_KEY:
    print("Fatal Error: API Key is missing!")
    print("Please check your .env file and ensure variable 'api_key' exists.")
    exit()

genai.configure(api_key=API_KEY)


model_name = 'models/gemini-flash-latest'
model = genai.GenerativeModel(model_name)

# ----------------------------
# 2. Gemini 분석 함수 (기존 프롬프트 유지)
# ----------------------------
def analyze_team(team_name, text_data):
    if not text_data: return None
    
    text_data = text_data[:1000] # 글자 수 제한 설정
    
    prompt = f"""
    너는 스포츠 데이터 분석가야. 텍스트를 분석하여 '{team_name}'의 성향 데이터를 JSON으로 추출해. 
    대상 종목은 [축구(EPL, K리그), 야구(KBO), 모터스포츠(F1)] 중 하나야.

    [필수 규칙]
    1. 오직 JSON 형식만 출력해. (마크다운 ```json 금지)
    2. 점수는 0점부터 10점 사이의 정수야. 특히 아래 제공된 [비교 대상 팀 리스트]에 속한 팀들과 상대적으로 비교하여, 각 지표의 점수 분포(Variance)가 겹치지 않고 변별력 있게 드러나도록 채점해.
    3. 아래 [범용 채점 기준]을 종목에 맞게 해석해서 적용해.
    4. team_name은 반드시 '한글'로 출력해.

    [데이터 생성 조건]
    1. style_tags: 팀의 특징을 잘 나타내는 영문 키워드 15개를 생성해. (이 키워드들은 웹 출력 시 한글로 번역되어 사용될 예정임)
    2. league: 반드시 ['EPL', 'K league', 'F1', 'KBO'] 중 하나를 선택해.
    3. sport: 반드시 ['축구', '야구', '모터스포츠'] 중 하나를 선택해.

    [비교 대상 팀 리스트]
    - EPL: 브라이튼 앤 호브 알비온, 리버풀, 토트넘 홋스퍼, 크리스탈 팰리스, 첼시, 뉴캐슬 유나이티드, 아스톤 빌라, 웨스트햄 유나이티드, 맨체스터 시티, 울버햄튼 원더러스, 아스널, 맨체스터 유나이티드
    - F1: 레드불, 레이싱 불스, 맥라렌, 메르세데스, 알핀, 애스턴 마틴, 윌리엄스, 자우버, 페라리, 하스
    - K league: 강원FC, 광주FC, 대구FC, 대전 하나 시티즌, FC서울, 수원 삼성 블루윙즈, FC안양, 울산 HD FC, 인천 유나이티드 FC, 전북 현대 모터스, 제주 유나이티드 FC, 포항 스틸러스
    - KBO: KT 위즈, LG 트윈스, NC 다이노스, SSG 랜더스, KIA 타이거즈, 두산 베어스, 롯데 자이언츠, 삼성 라이온즈, 키움 히어로즈, 한화 이글스

    [범용 채점 기준 (0~10점)]
    1. strength (전력/성적)
    2. money (자본력/예산)
    3. star_power (스타성)
    4. attack_style (경기 운영 스타일: 화끈함 vs 실리)
    5. underdog_feel (도전자/반란의 이미지)
    6. fan_passion (팬덤 화력)
    7. tradition (역사/헤리티지)

    [출력 JSON 포맷]
    {{
    "league": "EPL | K league | F1 | KBO",
    "sport": "축구 | 야구 | 모터스포츠",
    "team_name": "한글 팀명",
    "home_city": "string or null",
    "home_stadium": "string or null",
    "founded_year": number or null,
    "style_tags": ["Keyword1", "Keyword2", ..., "Keyword15"],
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
        print(f"'{team_name}' 분석 중 오류 발생: {e}")
        return None

# ----------------------------
# 3. 메인 실행부 (파일 로드 및 저장)
# ----------------------------
if __name__ == "__main__":
    source_dir = r"" # 분석할 폴더
    output_dir = r"" # 분석된 결과를 담을 새 폴더
    
    # 결과 저장용 폴더가 없으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(source_dir):
        print(f"경로를 찾을 수 없습니다: {source_dir}")
    else:
        files = [f for f in os.listdir(source_dir) if f.endswith('.txt')]
        print(f"총 {len(files)}개 팀 데이터 분석 시작")

        for file_name in files:
            team_name = file_name.replace('.txt', '').replace('_merge', '')
            save_path = os.path.join(output_dir, f"{team_name}.json")
            
            # 이미 분석된 파일이 있다면 건너뛰기 (시간/비용 절약)
            if os.path.exists(save_path):
                print(f"이미 분석됨: {team_name}")
                continue

            file_path = os.path.join(source_dir, file_name)
            print(f"\n[분석 중] {team_name}...")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            result = analyze_team(team_name, content)
            
            if result:
                # 분석 직후 개별 파일로 즉시 저장
                with open(save_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"{team_name} 저장 완료 -> {save_path}")
            time.sleep(60) # 할당량 초과 시 충분히 대기
        
            time.sleep(12) # 안전하게 분당 5회 정도로 요청 속도 조절


        print("\n" + "="*50)
        print(f"모든 팀 개별 분석 완료! 폴더: {output_dir}")
        print("="*50)