import os
import json
import pandas as pd
import numpy as np
import networkx as nx
import joblib
import warnings
from node2vec import Node2Vec
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings("ignore")

# ---------------------------------------------------------
# 1. 아티팩트 및 환경 설정
# ---------------------------------------------------------
DATA_DIR = r'./JSON 모음'
model_nlp = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')

# 수동 점수 가중치 (score.py 기준 보존)
ALPHA, BETA, GAMMA = 0.4, 0.4, 0.2

LEAGUE_MAP = {
    "K리그": "K league",
    "EPL": "EPL",
    "KBO": "KBO",
    "F1": "F1"
}

# [핵심] model50에서 저장한 아티팩트 로드
try:
    # 파일명이 일치하는지 확인하세요 (model50에서 저장한 이름)
    artifacts = joblib.load('sports_chatbot_model50.joblib')
    final_model = artifacts['final_model']
    pca = artifacts['pca']
    scaler = artifacts['scaler']
    le_league = artifacts['le_league']
    le_team = artifacts['le_team']
    input_features = artifacts['input_features'] # 학습 피처 리스트
    print("✅ 모델 및 전처리 아티팩트(model50) 로드 완료")
except Exception as e:
    print(f"❌ 로드 실패 (파일명이나 경로를 확인하세요): {e}")
    exit()

# model.py에서 정의한 PCA 한글 컬럼명
pca_named_cols = ["팬덤정체성_pca0", "스타성과강함_pca1", "명문과기적_pca2", "비주얼과매력_pca3", "자본과지배력_pca4"]

# ---------------------------------------------------------
# 2. 데이터 로딩 및 N2V 구축 (기존 로직 유지)
# ---------------------------------------------------------
def load_teams(path):
    teams = []
    if not os.path.exists(path): return teams
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith('.json'):
                with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
                    teams.append(json.load(f))
    return teams

def build_n2v_model(teams_data):
    G = nx.Graph()
    for t in teams_data:
        if 'team_name' in t: G.add_node(t['team_name'])
    
    for i in range(len(teams_data)):
        for j in range(i + 1, len(teams_data)):
            tags1 = set(teams_data[i].get('style_tags', []))
            tags2 = set(teams_data[j].get('style_tags', []))
            common = len(tags1.intersection(tags2))
            if common > 0:
                G.add_edge(teams_data[i]['team_name'], teams_data[j]['team_name'], weight=common)
    
    n2v = Node2Vec(G, dimensions=64, walk_length=10, num_walks=40, workers=1, quiet=True)
    return n2v.fit(window=5, min_count=1)

print("🚀 데이터 분석 및 네트워크 구성 중...")
teams_master = load_teams(DATA_DIR)
n2v_model = build_n2v_model(teams_master)

# ---------------------------------------------------------
# 3. 실시간 점수 계산 (시나리오 로직 보존)
# ---------------------------------------------------------
def get_scores_strict(query, anchor_name, candidate):
    # (1) sbert_score
    cand_tags = " ".join(candidate.get('style_tags', []))
    embs = model_nlp.encode([query, cand_tags])
    s_sem = cosine_similarity([embs[0]], [embs[1]])[0][0]

    # (2) n2v_score
    s_rel = 0.5
    if anchor_name and anchor_name in n2v_model.wv and candidate['team_name'] in n2v_model.wv:
        s_rel = n2v_model.wv.similarity(anchor_name, candidate['team_name'])

    # (3) vector_score (시나리오 가중치 적용)
    ts = candidate.get('scores', {})
    metrics = ['strength', 'money', 'star_power', 'attack_style', 'underdog_feel', 'fan_passion', 'tradition']
    t_vec = np.array([ts.get(m, 10) for m in metrics])
    
    target_vec = np.array([10]*7)
    s_multiplier = 1.0

    if any(k in query for k in ["언더독", "기적", "저비용", "머니볼", "효율", "가성비"]):
        target_vec[4] = 50
        if ts.get('money', 10) >= 16: s_multiplier = 0.3
        elif ts.get('money', 10) <= 8: s_multiplier = 1.5
    elif any(k in query for k in ["강한", "압도적", "최강", "부자"]):
        target_vec[0], target_vec[1] = 40, 40
        if ts.get('strength', 10) < 12: s_multiplier = 0.4
    elif any(k in query for k in ["미남", "잘생긴", "비주얼", "얼굴", "입덕"]):
        target_vec[2] = 50
        if ts.get('star_power', 10) < 12: s_multiplier = 0.4
    elif any(k in query for k in ["전통", "명문", "역사", "연고지", "자부심"]):
        target_vec[6], target_vec[5] = 40, 40
        if ts.get('tradition', 10) < 10: s_multiplier = 0.5
    elif any(k in query for k in ["공격", "화끈", "득점", "홈런", "추월", "시원시원"]):
        target_vec[3] = 50
        if ts.get('attack_style', 10) < 12: s_multiplier = 0.5
    elif any(k in query for k in ["수비", "단단한", "실리", "역습", "질식"]):
        target_vec[4], target_vec[0] = 30, 30
        if ts.get('attack_style', 10) > 15: s_multiplier = 0.5
    
    s_vec = cosine_similarity(target_vec.reshape(1, -1), t_vec.reshape(1, -1))[0][0]
    s_vec = s_vec * s_multiplier
    
    return s_sem, s_rel, s_vec

# ---------------------------------------------------------
# 4. 하이브리드 추천 서비스 (model50 동기화 버전)
# ---------------------------------------------------------
def recommend_service(query, user_type, support_team, target_league):
    # 리그명 표준화
    json_league_name = LEAGUE_MAP.get(target_league, target_league)
    candidates = [t for t in teams_master if t.get('league', '').lower() == json_league_name.lower()]
    
    if not candidates: return f"'{target_league}' 리그 정보를 찾을 수 없습니다."

    # A. 질문 임베딩 및 PCA 변환 (의도 추출)
    query_emb = model_nlp.encode([query])
    query_pca = pca.transform(query_emb)[0]

    rows = []
    for cand in candidates:
        s_sem, s_rel, s_vec = get_scores_strict(query, support_team, cand)
        
        # 수동 점수 (0.4, 0.4, 0.2)
        manual_score = (s_sem * ALPHA) + (s_rel * BETA) + (s_vec * GAMMA)

        row = {
            'team_name': cand['team_name'],
            'user_type': int(user_type),
            'recommend_league': json_league_name,
            'sbert_score': s_sem,
            'n2v_score': s_rel,
            'vector_score': s_vec,
            'manual_match_score': manual_score
        }
        # PCA 피처를 한글 컬럼명으로 추가 (model50 호환)
        for i, col_name in enumerate(pca_named_cols):
            row[col_name] = query_pca[i]
        rows.append(row)

    df_inf = pd.DataFrame(rows)

    # B. 전처리 (학습 단계와 일치)
    # 1) 리그 인코딩
    try:
        df_inf['recommend_league_enc'] = le_league.transform(df_inf['recommend_league'].astype(str))
    except:
        df_inf['recommend_league_enc'] = 0

    # 2) 점수 스케일링 및 '_mm' 컬럼 생성
    score_raw = ['sbert_score', 'n2v_score', 'vector_score']
    scaled_values = scaler.transform(df_inf[score_raw])
    
    df_inf['sbert_score_mm'] = scaled_values[:, 0]
    df_inf['n2v_score_mm'] = scaled_values[:, 1]
    df_inf['vector_score_mm'] = scaled_values[:, 2]

    # C. ML 모델 예측
    # [중요] input_features의 순서와 이름을 정확히 맞춥니다.
    X_input = df_inf[input_features]
    
    # 범주형 타입 지정
    cat_cols = ['user_type', 'recommend_league_enc']
    for col in cat_cols:
        if col in X_input.columns:
            X_input[col] = X_input[col].astype('category')

    df_inf['predict_score'] = final_model.predict(X_input)

    # D. 하이브리드 결합 (수동 0.8 : 모델 0.2) - 팀의 판단에 따라 조정 가능
    df_inf['final_score'] = (df_inf['manual_match_score'] * 0.8) + (df_inf['predict_score'] * 0.2)

    return df_inf.sort_values(by='final_score', ascending=False)

# ---------------------------------------------------------
# 5. 실행부
# ---------------------------------------------------------
print("\n" + "="*50)
user_q = input("💬 선호하는 스포츠 스타일은 무엇인가요?: ")
ut = input("💬 스포츠 팬 여부 (1:팬, 0:초보): ")
my_team = input("💬 응원 팀 (없으면 엔터): ") if ut == '1' else None
target = input("💬 추천받고 싶은 리그 (EPL/K리그/KBO/F1): ")

res = recommend_service(user_q, ut, my_team, target)

if isinstance(res, str):
    print(f"\n⚠️ {res}")
else:
    print(f"\n✨ '{target}' 리그 하이브리드 추천 순위:")
    for i, row in enumerate(res.head(5).itertuples(), 1):
        star = "⭐" if i <= 3 else "  "
        print(f"{star} {i}위: {row.team_name} (총점: {row.final_score:.4f})")
        print(f"    - 시나리오 점수: {row.manual_match_score:.4f}, AI 예측 점수: {row.predict_score:.4f}")