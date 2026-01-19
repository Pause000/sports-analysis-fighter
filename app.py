from flask import Flask, render_template, request, jsonify, send_from_directory
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

app = Flask(__name__, static_folder='web/static', template_folder='web/templates')

# ---------------------------------------------------------
# 1. 아티팩트 및 환경 설정
# ---------------------------------------------------------
# 실행 위치에 따라 조정 필요할 수 있음. 현재는 프로젝트 루트 실행 가정.
# 주소를 고쳐야합니다.
DATA_DIR = './JSON'
MODEL_PATH = './sports_chatbot_model50.joblib'

# 모델 로딩 (전역 변수로 한 번만 로드)
print("🔍 SBERT 모델(KR-SBERT) 로딩 중...")
 
try:
    model_nlp = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')
except Exception as e:
    print(f"Warning: Failed to load SBERT model: {e}")
    model_nlp = None



ALPHA, BETA, GAMMA = 0.4, 0.4, 0.2

LEAGUE_MAP = {
    "K리그": "K LEAGUE", "EPL": "EPL", "KBO": "KBO", "F1": "F1",
    "kleague": "K LEAGUE", "epl": "EPL", "kbo": "KBO", "f1": "F1"
}

# 전역 변수 초기화
artifacts = {}
final_model = None
pca = None
scaler = None
le_league = None
le_team = None
input_features = None
teams_master = []
n2v_model = None

def load_resources():
    global artifacts, final_model, pca, scaler, le_league, le_team, input_features, teams_master, n2v_model
    
    # 1. Joblib 아티팩트 로드
    if os.path.exists(MODEL_PATH):
        try:
            artifacts = joblib.load(MODEL_PATH)
            final_model = artifacts.get('final_model')
            pca = artifacts.get('pca')
            scaler = artifacts.get('scaler')
            le_league = artifacts.get('le_league')
            le_team = artifacts.get('le_team')
            input_features = artifacts.get('input_features')
            print("✅ 모델 및 전처리 아티팩트 로드 완료")
        except Exception as e:
            print(f"❌ 아티팩트 로드 실패: {e}")
    else:
        print(f"❌ 모델 파일 없음: {MODEL_PATH}")

    # 2. 데이터 로딩
    teams_master = load_teams(DATA_DIR)
    
    # 3. N2V 모델 구축
    if teams_master:
        n2v_model = build_n2v_model(teams_master)
    else:
        print("❌ 팀 데이터를 찾을 수 없습니다.")

def load_teams(path):
    teams = []
    if not os.path.exists(path): return teams
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
                        teams.append(json.load(f))
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
    return teams

def build_n2v_model(teams_data):
    print("🚀 N2V 모델 구축 중...")
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

# ---------------------------------------------------------
# 로직 함수
# ---------------------------------------------------------
def get_scores_strict(query, anchor_name, candidate):
    # (1) sbert_score
    cand_tags = " ".join(candidate.get('style_tags', []))
    if model_nlp:
        embs = model_nlp.encode([query, cand_tags])
        s_sem = cosine_similarity([embs[0]], [embs[1]])[0][0]
    else:
        s_sem = 0

    # (2) n2v_score
    s_rel = 0.5
    if n2v_model and anchor_name and anchor_name in n2v_model.wv and candidate['team_name'] in n2v_model.wv:
        s_rel = n2v_model.wv.similarity(anchor_name, candidate['team_name'])

    # (3) vector_score
    ts = candidate.get('scores', {})
    metrics = ['strength', 'money', 'star_power', 'attack_style', 'underdog_feel', 'fan_passion', 'tradition']
    t_vec = np.array([ts.get(m, 10) for m in metrics])
    
    target_vec = np.array([10]*7)
    s_multiplier = 1.0

    # 시나리오 로직
    if any(k in query for k in ["언더독", "기적", "저비용", "머니볼", "효율", "가성비"]):
        target_vec[4] = 50
        if ts.get('money', 10) >= 16: s_multiplier = 0.3
        elif ts.get('money', 10) <= 8: s_multiplier = 1.5
    elif any(k in query for k in ["강한", "압도적", "최강", "우승", "부자"]):
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

def recommend_service_logic(query, user_type, support_team, target_league):
    json_league_name = LEAGUE_MAP.get(target_league, target_league)
    
    candidates = [t for t in teams_master if t.get('league', '').lower() == json_league_name.lower()]
    if not candidates:
        return {"error": f"'{target_league}'에 해당하는 팀을 찾을 수 없습니다."}

    if pca and model_nlp:
        query_pca = pca.transform(model_nlp.encode([query]))[0]
    else:
        query_pca = np.zeros(5) # Fallback

    pca_cols = ['의도_팬덤정체성', '의도_스타성과강함', '의도_명문과기적', '의도_비주얼과매력', '의도_자본과지배력']

    rows = []
    for cand in candidates:
        s_sem, s_rel, s_vec = get_scores_strict(query, support_team, cand)
        
        manual_match_score = (s_sem * ALPHA) + (s_rel * BETA) + (s_vec * GAMMA)

        row = {
            'matching_team': cand['team_name'],
            'user_type': int(user_type),
            'recommend_league': json_league_name,
            'sbert_score': s_sem,
            'n2v_score': s_rel,
            'vector_score': s_vec,
            'manual_match_score': manual_match_score,
            # 추가 정보 전달을 위해 원본 데이터 일부 포함
            'team_data': cand 
        }
        for i, col in enumerate(pca_cols): row[col] = query_pca[i]
        rows.append(row)

    df_inf = pd.DataFrame(rows)
    
    if le_league:
        df_inf['recommend_league_enc'] = le_league.transform(df_inf['recommend_league'].astype(str))
    
    if scaler:
        score_cols = ['sbert_score', 'n2v_score', 'vector_score']
        scaled = scaler.transform(df_inf[score_cols])
        df_inf['sbert_score_mm'], df_inf['n2v_score_mm'], df_inf['vector_score_mm'] = scaled[:,0], scaled[:,1], scaled[:,2]

    if final_model and input_features:
        X_input = df_inf[input_features]
        cat_cols = [c for c in ["user_type", "recommend_league_enc"] if c in input_features]
        for c in cat_cols: X_input[c] = X_input[c].astype('category')
        
        df_inf['predict_score'] = final_model.predict(X_input)
    else:
        df_inf['predict_score'] = 0

    # Hybrid Score
    df_inf['final_hybrid_score'] = (df_inf['manual_match_score'] * 0.8) + (df_inf['predict_score'] * 0.2)
    
    # Sort
    df_result = df_inf.sort_values(by='final_hybrid_score', ascending=False)
    
    # Return top 3 results
    top_team = df_result.iloc[0]
    
    # 2등, 3등 추출 (데이터가 충분할 경우)
    others = []
    if len(df_result) > 1:
        for i in range(1, min(3, len(df_result))):
            row = df_result.iloc[i]
            others.append({
                "name": row['matching_team'],
                "match_percent": int(row['manual_match_score'] * 100) if row['manual_match_score'] > 0 else 0,
                "slogan": row['team_data'].get('introduction', '')[:20] + "..." if row['team_data'].get('introduction') else "",
                "score": float(row['final_hybrid_score'])
            })

    return {
        "team_name": top_team['matching_team'],
        "score": float(top_team['final_hybrid_score']),
        # 100점 만점 환산 (단순 예시)
        "match_percent": int(top_team['manual_match_score'] * 100) if top_team['manual_match_score'] > 0 else 0,
        "team_data": top_team['team_data'],
        "scores": {
            "passion": top_team['team_data']['scores'].get('fan_passion', 50) / 20 * 100,
            "money": top_team['team_data']['scores'].get('money', 50) / 20 * 100,
            "strategy": top_team['team_data']['scores'].get('attack_style', 50) / 20 * 100,
            "history": top_team['team_data']['scores'].get('tradition', 50) / 20 * 100,
            "star": top_team['team_data']['scores'].get('star_power', 50) / 20 * 100,
            "vibe": top_team['team_data']['scores'].get('underdog_feel', 50) / 20 * 100
        },
        "insight": top_team['team_data'].get('meta_description') or top_team['team_data'].get('introduction') or '추천 팀에 대한 설명이 없습니다.',
        "others": others # ✅ 2,3등 정보 추가
    }


# ---------------------------------------------------------
# Flask 라우트
# ---------------------------------------------------------
@app.before_request
def startup():
    if final_model is None:
        load_resources()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('web/images', filename)

@app.route('/chat', methods=['POST'])
def chat():
    # 1) JSON 요청인지 확인
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    # 2) 프론트에서 넘어온 데이터 받기
    data = request.get_json()

    ## 3) 리그 / 최종쿼리 / 좋아하는팀 관련 값 꺼내기
    league = data.get('league')  # 예: "epl", "kleague", "kbo", "f1"

    # ✅ 방향2: finalQuery는 객체로 받는다
    final_query_obj = data.get('finalQuery', {})  # 예: {"tokens":[...], "full_query":"..."}

    vibe = data.get('vibe')  # (구버전 호환용)

    # 4) 사용자 타입/응원팀(앵커팀) 설정
    favorite_team_exists = data.get('favoriteTeamExists', '')
    favorite_team = data.get('favoriteTeam', None)

    user_type = 1 if favorite_team_exists == "yes" else 0
    support_team = favorite_team if favorite_team_exists == "yes" else None

    # 5) ✅ 최종 모델 입력 query 결정 (우선순위: finalQuery.full_query > vibe > 기본값)
    vibe_map = {
        'aggressive': '공격적이고 화끈한 팀',
        'traditional': '전통과 역사가 있는 명문 팀',
        'star': '스타 선수가 많은 화려한 팀',
        'underdog': '약하지만 성장하는 언더독'
    }

    query = ""
    if isinstance(final_query_obj, dict):
        query = (final_query_obj.get("full_query") or "").strip()

    # full_query가 비어있으면 tokens로라도 이어붙이기
    if not query and isinstance(final_query_obj, dict):
        tokens = final_query_obj.get("tokens", [])
        if isinstance(tokens, list):
            query = " ".join([str(t) for t in tokens]).strip()

    # 그래도 비어 있으면 vibe fallback
    if not query:
        query = vibe_map.get(vibe, vibe) if vibe else "추천"

    print(f"[CHAT] league={league} user_type={user_type} support_team={support_team}")
    print(f"[CHAT] MODEL_INPUT_QUERY = {query}")

    # 6) 추천 로직 실행
    try:
        result = recommend_service_logic(
            query=query,
            user_type=user_type,
            support_team=support_team,
            target_league=league
        )

        if "error" in result:
            return jsonify(result), 404

        return jsonify(result)

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # 로컬 개발용
    load_resources() # Run immediately for dev
    app.run(host='0.0.0.0', port=5000, debug=True)
