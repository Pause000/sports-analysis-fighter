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
# 1. 초기 설정 및 가중치
# ---------------------------------------------------------
DATA_DIR = r'C:\project\sports-analysis-fighter\JSON 모음'  # ✅ JSON 폴더 경로
ALPHA, BETA, GAMMA = 0.4, 0.4, 0.2                     # ✅ 통합 점수 가중치
model_nlp = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')  # ✅ SBERT 모델 로드


# ---------------------------------------------------------
# 2. 데이터 로드 로직 (JSON 내부 league/sport/style_tags/scores 사용)
# ---------------------------------------------------------
def load_teams(path):
    teams = []  # ✅ 모든 팀 JSON 정보를 담을 리스트
    if not os.path.exists(path):  # ✅ 폴더가 없으면 즉시 종료
        print(f"❌ 경로 오류: '{path}'")
        return teams

    for root, dirs, files in os.walk(path):  # ✅ 폴더 내부를 전부 탐색
        for filename in files:               # ✅ 각 파일에 대해 반복
            if not filename.endswith('.json'):  # ✅ json만 사용
                continue

            full_path = os.path.join(root, filename)  # ✅ 파일의 전체 경로
            with open(full_path, 'r', encoding='utf-8') as f:  # ✅ 파일 열기
                try:
                    data = json.load(f)  # ✅ JSON 로드
                    if isinstance(data, list):  # ✅ 리스트 형태면 첫 번째만 사용
                        data = data[0]

                    # ✅ 파일명 기반 고유 팀명
                    data['team_name_unique'] = filename.replace('.json', '')

                    # ✅ JSON 내부 메타데이터 사용
                    data['league'] = data.get('league', '').upper()
                    data['sport'] = data.get('sport', '')

                    # ✅ scores 키 정리 (혹시 공백/콜론 있으면 정규화)
                    if 'scores' in data:
                        data['scores'] = {k.strip().replace(':', ''): v for k, v in data['scores'].items()}

                    teams.append(data)  # ✅ 팀 데이터 추가

                except Exception as e:
                    print(f"❌ 읽기 실패({filename}): {e}")

    return teams


# ---------------------------------------------------------
# 3. other_sports_info 생성 (팀 -> style_tags 매핑)
# ---------------------------------------------------------
def build_other_sports_info_from_teams(teams_data):
    other_sports_info = {}  # ✅ {team_name_unique: [style_tags...]}
    for t in teams_data:    # ✅ 모든 팀을 돌면서
        team_name = t.get("team_name_unique")       # ✅ 팀 이름
        style_tags = t.get("style_tags", [])        # ✅ 팀 스타일 태그
        if team_name and isinstance(style_tags, list) and len(style_tags) > 0:
            other_sports_info[team_name] = style_tags  # ✅ 매핑 저장
    return other_sports_info


# ---------------------------------------------------------
# 4. Node2Vec 관계망 학습 (공통 style_tags 기반 그래프)
# ---------------------------------------------------------
def train_node2vec(data):
    G = nx.Graph()  # ✅ 무방향 그래프 생성

    for i in range(len(data)):                 # ✅ 팀 i 반복
        for j in range(i + 1, len(data)):      # ✅ 팀 j 반복 (i+1부터, 중복 방지)
            common_tags = set(data[i].get('style_tags', [])) & set(data[j].get('style_tags', []))  # ✅ 교집합 태그
            if common_tags:  # ✅ 공통 태그가 있으면 엣지 생성
                G.add_edge(
                    data[i]['team_name_unique'],       # ✅ 노드 A
                    data[j]['team_name_unique'],       # ✅ 노드 B
                    weight=len(common_tags)            # ✅ 공통 태그 개수를 가중치로
                )

    if len(G.nodes) < 2:  # ✅ 그래프가 너무 작으면 학습 불가
        return None

    node2vec = Node2Vec(G, dimensions=64, walk_length=10, num_walks=40, workers=1)  # ✅ Node2Vec 설정 workers : cpu 코어 사용 개수, os.cpu_count() 사용시 모든 코어 사용
    return node2vec.fit(window=5, min_count=1)  # ✅ 임베딩 학습 후 모델 반환


# ---------------------------------------------------------
# 5. ✅ 시나리오 생성 (응원팀 있는 경우만)
#    - 팀별 style_tags(최대 20개) 중 랜덤 1개씩 "10번" (팀 내 중복 X)
#    - 질문 문장은 style_tags만 사용
# ---------------------------------------------------------
def build_fan_only_scenarios(other_sports_info, repeats_per_team=1): # ctrl + f 후 reaptes_per_team 숫자 둘다 바꾸기 
    scenarios = []  # ✅ 시나리오 리스트

    for fav_team, tags in other_sports_info.items():  # ✅ 팀별로 반복
        if not isinstance(tags, list) or len(tags) == 0:  # ✅ 태그 없으면 스킵
            continue

        k = min(repeats_per_team, len(tags))  # ✅ 태그가 10개 미만이면 그 수만큼만
        picked_tags = random.sample(tags, k=k)  # ✅ 중복 없이 태그 k개 뽑기

        for tag in picked_tags:  # ✅ 뽑힌 태그마다 질문 1개 생성
            query = (
                f"나는 {fav_team}의 '{tag}' 같은 스타일이 마음에 들어. "
                f"이런 느낌을 가진 다른 리그 팀을 추천해줘."
            )

            scenarios.append({
                "user_type": "1",     # ✅ 응원팀 있는 유저만
                "anchor": fav_team,   # ✅ 기준(기존 응원팀)
                "query": query        # ✅ 질문
            })

    return scenarios


# ---------------------------------------------------------
# 6. 통합 점수 계산 함수 (기존 로직 유지)
# ---------------------------------------------------------
def calculate_integrated_score(anchor_team, user_query, candidate_team, n2v_model, all_teams):
    cand_name = candidate_team['team_name_unique']  # ✅ 후보 팀 이름
    cand_league = candidate_team.get('league', '').upper()  # ✅ 후보 팀 리그

    # [A] 본인 제외
    if anchor_team and anchor_team != "None":
        if anchor_team.replace(" ", "").upper() in cand_name.replace(" ", "").upper():
            return 0.0

    # [B] Semantic Score (SBERT): 질문 vs 후보팀 style_tags
    tags_str = " ".join(candidate_team.get('style_tags', []))  # ✅ 후보팀 태그를 하나의 문장으로
    emb = model_nlp.encode([user_query, tags_str])              # ✅ 질문/태그 임베딩
    s_semantic = cosine_similarity([emb[0]], [emb[1]])[0][0]    # ✅ 코사인 유사도

    # [C] Relational Score (Node2Vec): 앵커팀 vs 후보팀 관계 점수
    s_relational = 0.5  # ✅ 기본값
    if anchor_team and anchor_team != "None" and n2v_model:
        try:
            if anchor_team in n2v_model.wv and cand_name in n2v_model.wv:
                s_relational = n2v_model.wv.similarity(anchor_team, cand_name)  # ✅ 노드 유사도
        except:
            pass

    # [D] Vector Score: scores 기반
    ts = candidate_team.get('scores', {})  # ✅ 후보팀 점수 dict
    t_vec = np.array([ts.get(k, 10) for k in ['strength', 'money', 'star_power', 'attack_style',
                                              'underdog_feel', 'fan_passion', 'tradition']])  # ✅ 7차원 벡터

    # ✅ 리그별 가중치
    l_weight = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    if 'F1' in cand_league:
        l_weight = np.array([1.5, 1.5, 1.3, 1.0, 1.0, 0.7, 0.5])
    elif 'EPL' in cand_league:
        l_weight = np.array([1.3, 1.2, 1.1, 1.4, 1.0, 1.0, 1.0])
    elif 'KBO' in cand_league or 'K league' in cand_league:
        l_weight = np.array([1.0, 0.8, 1.0, 1.0, 1.2, 1.5, 1.5])

    weighted_t_vec = t_vec * l_weight  # ✅ 리그 가중치 적용
    target_vec = np.array([10, 10, 10, 10, 10, 10, 10])  # ✅ 기본 목표 벡터
    s_multiplier = 1.0  # ✅ 시나리오 키워드에 따른 보정값

    # ✅ 질문 키워드 기반 벡터 보정 (기존 유지)
    if any(k in user_query for k in ["언더독", "기적", "저비용", "머니볼", "효율", "가성비"]):
        target_vec[4] = 50
        if ts.get('money', 10) >= 16:
            s_multiplier = 0.3
        elif ts.get('money', 10) <= 8:
            s_multiplier = 1.5

    elif any(k in user_query for k in ["강한", "압도적", "최강", "우승", "부자"]):
        target_vec[0], target_vec[1] = 40, 40
        if ts.get('strength', 10) < 12:
            s_multiplier = 0.4

    elif any(k in user_query for k in ["미남", "잘생긴", "비주얼", "얼굴", "입덕"]):
        target_vec[2] = 50
        if ts.get('star_power', 10) < 12:
            s_multiplier = 0.4

    elif any(k in user_query for k in ["전통", "명문", "역사", "연고지", "자부심"]):
        target_vec[6], target_vec[5] = 40, 40
        if ts.get('tradition', 10) < 10:
            s_multiplier = 0.5

    elif any(k in user_query for k in ["공격", "화끈", "득점", "홈런", "추월", "시원시원"]):
        target_vec[3] = 50
        if ts.get('attack_style', 10) < 12:
            s_multiplier = 0.5

    elif any(k in user_query for k in ["수비", "단단한", "실리", "역습", "질식"]):
        target_vec[4], target_vec[0] = 30, 30
        if ts.get('attack_style', 10) > 15:
            s_multiplier = 0.5

    s_vector = cosine_similarity(target_vec.reshape(1, -1), weighted_t_vec.reshape(1, -1))[0][0]  # ✅ 벡터 유사도
    final_score = (ALPHA * s_semantic) + (BETA * s_relational) + (GAMMA * s_vector)  # ✅ 가중합
    return float(final_score * s_multiplier)  # ✅ 최종 점수 반환


# ---------------------------------------------------------
# 7. 실행 및 저장 (리그별 Top3, 기존 팬은 같은 리그 제외)
# ---------------------------------------------------------
teams_data = load_teams(DATA_DIR)  # ✅ JSON 데이터 로드
other_sports_info = build_other_sports_info_from_teams(teams_data)  # ✅ 팀->태그 매핑
n2v_model = train_node2vec(teams_data)  # ✅ Node2Vec 학습

# ✅ 응원팀 있는 경우만 + 팀당 태그 10개(중복X)
scenarios = build_fan_only_scenarios(other_sports_info, repeats_per_team=1) # 질문 개수

rows = []  # ✅ CSV에 들어갈 행 리스트

for scene in scenarios:
    # (A) 앵커 팀 league 찾기
    anchor_league = None
    for t in teams_data:
        if t["team_name_unique"] == scene["anchor"]:
            anchor_league = t.get("league", "").upper()
            break

    # (B) 리그별 후보 점수 모으기
    league_scores = {}  # ✅ {league: [(team_name, score), ...]}

    for candidate in teams_data:
        league = candidate.get("league", "").upper()

        score = calculate_integrated_score(
            scene["anchor"],
            scene["query"],
            candidate,
            n2v_model,
            teams_data
        )

        league_scores.setdefault(league, []).append((candidate["team_name_unique"], float(score)))

    # (C) 리그별 Top3 저장 (같은 리그 제외)
    for league, items in league_scores.items():
        if anchor_league == league:  # ✅ 같은 리그는 제외
            continue

        items.sort(key=lambda x: x[1], reverse=True)  # ✅ 점수 내림차순 정렬
        top3 = items[:3]  # ✅ Top3 자르기

        for team_name, s in top3:
            rows.append({
                "사용자 유형": scene["user_type"],
                "기존 응원 팀": "None" if scene["user_type"] == "0" else scene["anchor"],
                "질문": scene["query"],
                "매칭팀": team_name,
                "추천 리그": league,
                "매칭 스코어": float(s)
            })

df_out = pd.DataFrame(rows)  # ✅ DataFrame 변환
df_out.to_csv("test2.csv", index=False, encoding="utf-8-sig")  # ✅ CSV 저장
print("\n✅ 'test2.csv' 생성 완료!")

