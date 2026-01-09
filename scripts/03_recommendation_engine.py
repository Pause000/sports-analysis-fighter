import json
import pandas as pd
import numpy as np
import os
import random
import networkx as nx
from sentence_transformers import SentenceTransformer
from node2vec import Node2Vec
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------------------------------
# 1. 초기 설정 및 가중치 (기본값 유지)
# ---------------------------------------------------------
DATA_DIR = r'../database/json'  # 본인 환경에 맞게 수정
OUTPUT_DIR = r''
ALPHA, BETA, GAMMA = 0.4, 0.4, 0.2
model_nlp = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')

# ---------------------------------------------------------
# 2. 데이터 로드 로직 (수정 없음)
# ---------------------------------------------------------
def load_teams(path):
    teams = []
    if not os.path.exists(path):
        print(f"❌ 경로 오류: '{path}'")
        return teams
    for root, dirs, files in os.walk(path):
        for filename in files:
            if not filename.endswith('.json'): continue
            full_path = os.path.join(root, filename)
            with open(full_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list): data = data[0]
                    data['team_name_unique'] = filename.replace('.json', '')
                    data['league'] = data.get('league', '').upper()
                    data['sport'] = data.get('sport', '')
                    if 'scores' in data:
                        data['scores'] = {k.strip().replace(':', ''): v for k, v in data['scores'].items()}
                    teams.append(data)
                except Exception as e:
                    print(f"❌ 읽기 실패({filename}): {e}")
    return teams

def build_other_sports_info_from_teams(teams_data):
    other_sports_info = {}
    for t in teams_data:
        team_name = t.get("team_name_unique")
        style_tags = t.get("style_tags", [])
        if team_name and isinstance(style_tags, list) and len(style_tags) > 0:
            other_sports_info[team_name] = style_tags
    return other_sports_info

# ---------------------------------------------------------
# 3. 모델 학습 로직 (수정 없음)
# ---------------------------------------------------------
def train_node2vec(data):
    G = nx.Graph()
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            common_tags = set(data[i].get('style_tags', [])) & set(data[j].get('style_tags', []))
            if common_tags:
                G.add_edge(data[i]['team_name_unique'], data[j]['team_name_unique'], weight=len(common_tags))
    if len(G.nodes) < 2: return None
    node2vec = Node2Vec(G, dimensions=64, walk_length=10, num_walks=40, workers=1)
    return node2vec.fit(window=5, min_count=1)

# ---------------------------------------------------------
# 4. 시나리오 생성 로직 (응원팀 유무에 따른 개수 수정)
# ---------------------------------------------------------
def build_fan_only_scenarios(other_sports_info, num_samples=30):
    scenarios = []
    team_list = list(other_sports_info.keys())
    
    # 30개의 질문을 만들기 위해 팀 리스트에서 중복 허용하여 샘플링
    sampled_teams = random.choices(team_list, k=num_samples)
    
    for fav_team in sampled_teams:
        tags = other_sports_info[fav_team]
        if not tags: continue
        tag = random.choice(tags)
        query = f"나는 {fav_team}의 '{tag}' 같은 스타일이 마음에 들어. 이런 느낌을 가진 다른 리그 팀을 추천해줘."
        scenarios.append({"user_type": "1", "anchor": fav_team, "query": query})
    return scenarios

pref_dict = {
    "재정": ["머니볼", "가성비", "저비용", "효율", "부자"],
    "서사": ["언더독", "기적", "낭만", "신흥 강호", "역전"],
    "역사": ["전통", "명문", "역사", "연고지", "자부심"],
    "전술": ["공격", "화끈", "수비", "단단한", "역습", "실리", "조직력"],
    "인기": ["스타성", "팬덤", "미남", "잘생긴", "비주얼", "입덕"],
    "성과": ["우승", "강한", "우승권 유지", "압도적", "최강"]
}

def build_beginner_scenarios_from_dict(num_samples, pref_dict):
    scenarios = []
    intro_leagues = ["EPL", "KBO", "K LEAGUE", "F1"]
    categories = list(pref_dict.keys())
    for _ in range(num_samples):
        num_keys = random.choice([1, 2])
        selected_cats = random.sample(categories, k=num_keys)
        selected_prefs = [random.choice(pref_dict[cat]) for cat in selected_cats]
        pref_text = "와(과) ".join(selected_prefs)
        league = random.choice(intro_leagues)
        query = f"나는 {league}는 처음인데, {pref_text} 성향이 강한 팀을 추천해줘."
        scenarios.append({"user_type": "0", "anchor": "None", "query": query})
    return scenarios

# ---------------------------------------------------------
# 5. 점수 계산 로직 (수정 없음)
# ---------------------------------------------------------
def calculate_integrated_score(anchor_team, user_query, candidate_team, n2v_model, all_teams):
    cand_name = candidate_team['team_name_unique']
    cand_league = candidate_team.get('league', '').upper()

    if anchor_team and anchor_team != "None":
        if anchor_team.replace(" ", "").upper() in cand_name.replace(" ", "").upper():
            return 0.0, 0.0, 0.0, 0.0

    tags_str = " ".join(candidate_team.get('style_tags', []))
    emb = model_nlp.encode([user_query, tags_str])
    s_semantic = cosine_similarity([emb[0]], [emb[1]])[0][0]

    s_relational = 0.5
    if anchor_team and anchor_team != "None" and n2v_model:
        try:
            if anchor_team in n2v_model.wv and cand_name in n2v_model.wv:
                s_relational = n2v_model.wv.similarity(anchor_team, cand_name)
        except: pass

    ts = candidate_team.get('scores', {})
    t_vec = np.array([ts.get(k, 10) for k in ['strength', 'money', 'star_power', 'attack_style', 'underdog_feel', 'fan_passion', 'tradition']])
    
    l_weight = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    if 'F1' in cand_league: l_weight = np.array([1.5, 1.5, 1.3, 1.0, 1.0, 0.7, 0.5])
    elif 'EPL' in cand_league: l_weight = np.array([1.3, 1.2, 1.1, 1.4, 1.0, 1.0, 1.0])
    elif 'KBO' in cand_league or 'K LEAGUE' in cand_league: l_weight = np.array([1.0, 0.8, 1.0, 1.0, 1.2, 1.5, 1.5])

    weighted_t_vec = t_vec * l_weight
    target_vec = np.array([10, 10, 10, 10, 10, 10, 10])
    s_multiplier = 1.0

    if any(k in user_query for k in ["언더독", "기적", "저비용", "머니볼", "효율", "가성비"]):
        target_vec[4] = 50
        if ts.get('money', 10) >= 16: s_multiplier = 0.3
        elif ts.get('money', 10) <= 8: s_multiplier = 1.5
    elif any(k in user_query for k in ["강한", "압도적", "최강", "우승", "부자"]):
        target_vec[0], target_vec[1] = 40, 40
        if ts.get('strength', 10) < 12: s_multiplier = 0.4
    elif any(k in user_query for k in ["미남", "잘생긴", "비주얼", "얼굴", "입덕"]):
        target_vec[2] = 50
        if ts.get('star_power', 10) < 12: s_multiplier = 0.4
    elif any(k in user_query for k in ["전통", "명문", "역사", "연고지", "자부심"]):
        target_vec[6], target_vec[5] = 40, 40
        if ts.get('tradition', 10) < 10: s_multiplier = 0.5
    elif any(k in user_query for k in ["공격", "화끈", "득점", "홈런", "추월", "시원시원"]):
        target_vec[3] = 50
        if ts.get('attack_style', 10) < 12: s_multiplier = 0.5
    elif any(k in user_query for k in ["수비", "단단한", "실리", "역습", "질식"]):
        target_vec[4], target_vec[0] = 30, 30
        if ts.get('attack_style', 10) > 15: s_multiplier = 0.5

    s_vector = cosine_similarity(target_vec.reshape(1, -1), weighted_t_vec.reshape(1, -1))[0][0]
    final_score = (ALPHA * s_semantic) + (BETA * s_relational) + (GAMMA * s_vector)
    
    return float(final_score * s_multiplier), s_semantic, s_relational, s_vector

# ---------------------------------------------------------
# 6. 실행 및 통합 저장 (추출 개수 및 모든 팀 결과 수정)
# ---------------------------------------------------------
teams_data = load_teams(DATA_DIR)
other_sports_info = build_other_sports_info_from_teams(teams_data)
n2v_model = train_node2vec(teams_data)

# [수정] 응원팀 있는 경우 30개, 없는 경우 70개 생성
fan_scenarios = build_fan_only_scenarios(other_sports_info, num_samples=50)
beginner_scenarios = build_beginner_scenarios_from_dict(num_samples=80, pref_dict=pref_dict)
all_scenarios = fan_scenarios + beginner_scenarios

rows = []
for scene in all_scenarios:
    user_type = scene["user_type"]
    anchor = scene["anchor"]
    query = scene["query"]

    anchor_league = None
    if user_type == "1":
        for t in teams_data:
            if t["team_name_unique"] == anchor:
                anchor_league = t.get("league", "").upper()
                break

    league_scores = {}
    for candidate in teams_data:
        league = candidate.get("league", "").upper()
        # 유저 타입 1(응원팀 있음)인 경우 같은 리그는 건너뜀 (나머지 3개 리그 추출)
        if user_type == "1" and league == anchor_league:
            continue

        score, s_sem, s_rel, s_vec = calculate_integrated_score(anchor, query, candidate, n2v_model, teams_data)
        league_scores.setdefault(league, []).append((candidate["team_name_unique"], score, s_sem, s_rel, s_vec))

    for league, items in league_scores.items():
        # 정렬은 수행하되, [:3] 제한을 제거하여 모든 팀을 추출하도록 수정
        items.sort(key=lambda x: x[1], reverse=True)
        for team_name, s, s_sem, s_rel, s_vec in items:
            rows.append({
                "사용자 유형": user_type,
                "기존 응원 팀": anchor,
                "질문": query,
                "매칭팀": team_name,
                "추천 리그": league,
                "sbert_score": s_sem,
                "n2v_score": s_rel,
                "vector_score": s_vec,
                "매칭 스코어": round(s, 4)
            })

if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
df_final = pd.DataFrame(rows)
df_final.to_csv(os.path.join(OUTPUT_DIR, "integrated_training_data.csv"), index=False, encoding="utf-8-sig")
print(f"✅ 통합 데이터 생성 완료! 총 {len(df_final)}행이 저장되었습니다.")