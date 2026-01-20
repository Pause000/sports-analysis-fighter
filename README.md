# 🏟️ Sports Team Matchmaker (내 취향저격 스포츠 팀 찾기)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white) 
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green?logo=flask&logoColor=white) 
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql&logoColor=white)
![AI](https://img.shields.io/badge/AI-SBERT%20%2B%20Node2Vec-purple)

> **"축구, 야구, F1... 남들은 재밌다는데 나는 어디를 응원해야 할까?"**  
> 이제 고민하지 마세요. 당신의 성향과 딱 맞는 '인생 팀'을 AI가 찾아드립니다!

---

## 📖 목차 (Table of Contents)
1.  [🔍 프로젝트 소개](#-프로젝트-소개)
2.  [🙋‍♀️ 누구에게 필요한가요?](#-누구에게-필요한가요)
3.  [✨ 주요 기능](#-주요-기능-key-features)
4.  [🧠 추천 알고리즘의 비밀](#-추천-알고리즘의-비밀)
5.  [🛠 사용된 기술 (Tech Stack)](#-사용된-기술-tech-stack)
6.  [💻 설치 및 실행 가이드](#-설치-및-실행-가이드)
7.  [📂 프로젝트 구조](#-프로젝트-구조-directory)
8.  [🧱 핵심 코드 분석](#-핵심-코드-분석-code-deep-dive)
9.  [👨‍💻 팀원 소개](#-팀원-소개)

---

## 🔍 프로젝트 소개
**Sports Team Matchmaker**는 스포츠에 입문하고 싶지만 어떤 팀을 응원해야 할지 몰라 망설였던 분들을 위한 **지능형 AI 챗봇 서비스**입니다.

복잡한 규칙이나 선수 이름을 몰라도 괜찮습니다. 평소 당신의 취향(예: "화끈한 공격이 좋아", "팬들의 열정이 중요해", "언더독의 기적을 믿어")만 이야기하면, **EPL(영국 축구), K리그(한국 축구), KBO(한국 야구), F1(포뮬러 1)** 리그 중에서 당신과 찰떡궁합인 팀을 추천해줍니다.

---

## 🙋‍♀️ 누구에게 필요한가요?
| 이런 분들에게 추천해요! 👍 | 이런 고민을 해결해드려요! 💡 |
| :--- | :--- |
| **스포츠 입문자** | "축구를 보고 싶은데, 팀이 너무 많아서 못 고르겠어요." |
| **타 종목 팬** | "야구팬인데, 축구도 요즘 재밌어 보이네? 내 야구 팀이랑 비슷한 축구 팀 없나?" |
| **데이터 덕후** | "단순히 성적순이 아니라, 데이터 기반으로 나랑 잘 맞는 팀을 찾고 싶어." |

---

## ✨ 주요 기능 (Key Features)

### 1️⃣ 친구처럼 대화하는 AI 챗봇 💬
딱딱한 설문조사가 아닙니다. 챗봇과 자연스럽게 대화하며 당신의 취향을 알려주세요.
> 🗣️ *"나는 가끔 지더라도 끝까지 물고 늘어지는 끈기 있는 팀이 좋아!"*  
> 🗣️ *"돈을 많이 써서라도 우승 컵을 들어 올리는 팀이 최고지!"*

### 2️⃣ 다양한 종목과 리그 지원 🌏
축구만 추천하지 않습니다. 국내외 인기 리그를 모두 지원합니다.
*   **⚽ EPL (프리미어리그):** 세계 최고 수준의 축구 리그
*   **⚽ K리그:** 내 고장, 내 팀! 한국 프로축구
*   **⚾ KBO:** 열광적인 응원 문화! 한국 프로야구
*   **🏎️ F1:** 0.001초의 승부! 모터스포츠의 정점

### 3️⃣ 눈이 즐거운 시각화 대시보드 📊
팀을 추천받으면, 그 팀의 매력을 한눈에 볼 수 있는 멋진 대시보드가 펼쳐집니다.
*   **🎯 추천 점수 & 매칭 이유:** 왜 이 팀이 당신에게 맞는지 AI가 분석한 결과를 알려줍니다.
*   **🎬 하이라이트 영상:** 팀의 분위기를 느낄 수 있는 주요 장면들을 바로 시청하세요.
*   **📝 팀 정보 & 선수:** 팀의 역사, 주요 선수, 최근 성적 등을 확인해 보세요.

---

## 🧠 추천 알고리즘의 비밀 
이 챗봇은 단순한 키워드 매칭이 아닙니다. **최신 AI 기술**을 활용해 당신의 숨겨진 취향까지 분석합니다.

### 🤖 3단계 하이브리드 추천 엔진
1.  **자연어 처리 (NLP - SBERT):**  
    "가난하지만 기적을 만드는"이라는 문장을 이해하여 '언더독', '효율성', '성장' 같은 핵심 가치를 추출합니다.
2.  **관계 분석 (Graph - Node2Vec):**  
    스포츠 세계의 복잡한 팀 관계(라이벌, 팀 컬러 유사성)를 그래프로 분석하여, 당신이 좋아하는 스타일과 유사한 '분위기(Vibe)'를 탐색합니다.
3.  **종합 스코어링 (Weighted Scoring):**  
    7가지 핵심 지표(`자본력`, `역사`, `팬덤`, `스타성` 등)를 기반으로 정교하게 계산하여 99%의 정확도를 목표로 합니다.

---

## 🛠 사용된 기술 스택 (Tech Stack)

### 🧱 Backend (Server & Database)
*   **Python 3.8+**: AI 라이브러리와의 호환성이 가장 뛰어난 언어로 선정했습니다.
*   **Flask**: 가볍고 유연한 마이크로 프레임워크로, AI 모델 서빙과 웹 서버 기능을 빠르게 구현하기 위해 채택했습니다.
*   **MySQL (SQLAlchemy)**: 사용자 정보와 팀 데이터의 관계형 구조를 안정적으로 관리하기 위해 사용했습니다.
*   **Flask-Login**: 세션 기반의 안전하고 간편한 사용자 인증 관리를 구현했습니다.

### 🤖 AI (Artificial Intelligence)
*   **Sentence-BERT (`sentence-transformers`)**: 
    *   단순 키워드 매칭의 한계를 넘어, 문맥적 의미(Context)를 파악하기 위해 사용했습니다.
    *   *"가난하지만 끈기 있는"* 같은 복합적인 성향을 벡터로 변환하여 팀과 비교합니다.
*   **Node2Vec (`networkx`, `node2vec`)**: 
    *   팀들 간의 보이지 않는 관계(라이벌, 팀 컬러, 스타일)를 그래프로 연결하고 학습시켰습니다.
    *   나의 성향과 그래프 상에서 가까운 거리에 있는 팀을 추천하는 데 활용됩니다.
*   **Scikit-learn & Pandas**: 데이터 전처리 및 코사인 유사도 계산 등 핵심 로직 구현에 사용되었습니다.

### 🎨 Frontend (Client)
*   **Vanilla JavaScript (ES6+)**: 
    *   무거운 프레임워크(React/Vue) 없이 브라우저 네이티브 기능만으로 빠르고 가벼운 SPA(Single Page Application) 같은 UX를 구현했습니다.
*   **HTML5 & CSS3**: 
    *   반응형 그리드 레이아웃과 Flexbox를 활용해 다양한 화면 크기에 대응하도록 디자인했습니다.

---

## 💻 설치 및 실행 가이드

### 1. 필수 프로그램 준비
*   [Python](https://www.python.org/) 설치 확인
*   [MySQL](https://www.mysql.com/) 설치 및 실행 확인

### 2. 프로젝트 다운로드 및 실행
별도의 패키지 설치 명령어를 입력할 필요가 없습니다. **실행 시 자동으로 환경을 구축합니다.**

```bash
# 1. 앱 실행
python app.py
```

> ⚠️ **최초 실행 시 주의사항:**  
> 처음 실행할 때는 필요한 AI 라이브러리를 설치하느라 시간이 조금 걸릴 수 있습니다 (약 1~3분).  
> "Dependencies installed successfully!" 메시지가 뜨고 앱이 재시작될 때까지 기다려주세요.

### 3. 서비스 접속
브라우저 주소창에 아래 주소를 입력하세요.
👉 `http://localhost:5000`

---

## 📂 프로젝트 구조 (Directory)
```
sports-analysis-fighter/
├── app.py                     # 🚀 메인 실행 파일 (서버 시작점)
├── database/                  # 💾 데이터베이스 관리
│   ├── models.py              # DB 테이블 구조 정의 (User, Team, Log)
│   └── extensions.py          # DB 연결 도구
├── scripts/                   # 🤖 AI 및 유틸리티 스크립트
│   ├── recommendation_engine.py  # 핵심 추천 알고리즘
│   └── setup_env.py           # 자동 환경 설정 스크립트
├── web/                       # 🎨 화면 구성 (프론트엔드)
│   ├── static/                # CSS, JS, 이미지 파일
│   └── templates/             # HTML 페이지
└── requirements.txt           # 📦 필요한 라이브러리 목록
```

---

## 🧱 Code Deep Dive (핵심 코드 분석)

프로젝트의 핵심이 되는 모델 서빙과 추천 로직의 실제 코드를 소개합니다.

### 1. 🚀 `app.py`: 하이브리드 추천 엔진 초기화
Flask 앱이 시작될 때, 무거운 NLP 모델(SBERT)과 그래프 모델(Node2Vec)을 메모리에 로드하여 실시간 추천을 준비합니다.

```python
# app.py (Line 72-79)

# 3. Recommendation Engine Initialization
# =========================================================
from scripts.recommendation_engine import RecommendationEngine

# 인스턴스 생성 시 데이터와 모델 경로를 지정합니다.
# 내부적으로 SBERT, Node2Vec, XGBoost/LGBM 모델을 관리합니다.
rec_engine = RecommendationEngine(
    data_dir='./database/JSON', 
    model_path='./fit_model.joblib'
)
```

### 2. 🧠 `recommendation_engine.py`: 3단계 점수 산출 로직
사용자의 입력(`query`)과 각 팀(`candidate`) 사이의 유사도를 세 가지 측면에서 분석하여 합산합니다.

```python
# scripts/recommendation_engine.py (Line 138)

def calculate_integrated_score(self, query, anchor_name, candidate):
    """
    1. Semantic Score: 사용자의 말과 팀 스타일 태그의 의미적 유사도 (SBERT)
    2. Relational Score: 좋아하는 팀(anchor)과 후보 팀 간의 그래프상 거리 (Node2Vec)
    3. Vector Score: 자본력, 공격성 등 7대 지표의 수치적 매칭 (Rule-based)
    """

    # 1. Semantic Score (NLP)
    # 사용자의 문장과 팀의 스타일 태그("닥공", "명문" 등)를 벡터로 변환해 비교
    if self.model_nlp:
        embs = self.model_nlp.encode([query, cand_tags])
        s_sem = cosine_similarity([embs[0]], [embs[1]])[0][0]

    # 2. Relational Score (Graph)
    # 기존에 좋아하는 팀이 있다면, 그 팀과 '유사한' 위치에 있는 팀을 찾음
    if self.n2v_model and anchor_name:
         s_rel = self.n2v_model.wv.similarity(anchor_name, candidate['team_name'])

    # 3. Vector Score (Weighted Logic)
    # "돈", "부자" 등의 키워드가 있으면 자본력(money) 지표에 가중치 부여
    if any(k in query for k in ["강한", "압도적", "최강", "우승", "부자"]):
        target_vec[0], target_vec[1] = 40, 40  # strength, money 점수 상향 기대

    return weighted_total_score, s_sem, s_rel, s_vec
```

### 3. 📡 `app.py`: `/chat` 라우트 (AI와 사용자 연결)
프론트엔드에서 받은 사용자 정보(선호 팀, 리그, 쿼리)를 엔진에 전달하고 결과를 반환합니다.

```python
# app.py (Line 240)

# 사용자의 자연어 입력(query)과 선호 정보(support_team)를 엔진에 전달
result = rec_engine.recommend(
    query=query,                # "공격적이고 화끈한 팀 추천해줘"
    user_type=user_type,        # 기존 팬 여부 (0 or 1)
    support_team=support_team,  # 기존 응원 팀 (Node2Vec의 시작점)
    target_league=league        # 추천받고 싶은 리그 (EPL, KBO 등)
)

if "error" in result:
    return jsonify(result), 404

return jsonify(result) # { "team_name": "리버풀", "reason": ..., "score": 98.5 }
```

---

## 👨‍💻 팀원 소개
**Sports Analysis Fighter Team**은 스포츠 데이터의 가치를 믿는 개발자들로 구성되어 있습니다.

*   👑 **강연우 (Leader / AI):** 추천 모델 아키텍처 설계, 핵심 알고리즘 구현
*   🛠 **신종환 (Backend):** 안정적인 서버 구축, 데이터베이스 스키마 설계
*   🎨 **조중현 (Frontend):** 사용자 경험(UX) 설계, 직관적인 인터페이스 개발
*   📊 **한정현 (Data Analyst):** 다종목 스포츠 데이터 수집, 전처리 파이프라인 구축

---

*Copyright © 2026 Sports Analysis Fighter. All rights reserved.*