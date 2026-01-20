
import json
import pandas as pd
import numpy as np
import os
import networkx as nx
import joblib
from sentence_transformers import SentenceTransformer
from node2vec import Node2Vec
from sklearn.metrics.pairwise import cosine_similarity
import warnings

warnings.filterwarnings("ignore")

class RecommendationEngine:
    """
    Core engine for Sports Team Recommendation Chatbot.
    Combines NLP (SBERT), Graph (Node2Vec), and Traditional ML (XGBoost/LGBM) scores.
    """
    def __init__(self, data_dir='./JSON', model_path='./sports_chatbot_model50.joblib'):
        """
        Initialize the engine with paths to data and model artifacts.
        """
        self.DATA_DIR = data_dir
        self.MODEL_PATH = model_path
        
        # Hyperparameters
        self.ALPHA = 0.4
        self.BETA = 0.4
        self.GAMMA = 0.2
        
        # Models and Data
        self.model_nlp = None
        self.n2v_model = None
        self.teams_master = []
        
        # Artifacts from Joblib
        self.final_model = None
        self.pca = None
        self.scaler = None
        self.le_league = None
        self.le_team = None
        self.input_features = None
        
        self.LEAGUE_MAP = {
            "K리그": "K LEAGUE", "EPL": "EPL", "KBO": "KBO", "F1": "F1",
            "kleague": "K LEAGUE", "epl": "EPL", "kbo": "KBO", "f1": "F1"
        }

    def load_resources(self):
        """
        Load heavy resources (SBERT, Joblib artifacts) and build the Node2Vec graph.
        Should be called once at startup.
        """
        print("🔍 SBERT 모델(KR-SBERT) 로딩 중...")
        try:
            self.model_nlp = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')
        except Exception as e:
            print(f"Warning: Failed to load SBERT model: {e}")
            self.model_nlp = None

        # 1. Joblib 아티팩트 로드
        if os.path.exists(self.MODEL_PATH):
            try:
                artifacts = joblib.load(self.MODEL_PATH)
                self.final_model = artifacts.get('final_model')
                self.pca = artifacts.get('pca')
                self.scaler = artifacts.get('scaler')
                self.le_league = artifacts.get('le_league')
                self.le_team = artifacts.get('le_team')
                self.input_features = artifacts.get('input_features')
                print("✅ 모델 및 전처리 아티팩트 로드 완료")
            except Exception as e:
                print(f"❌ 아티팩트 로드 실패: {e}")
        else:
            print(f"❌ 모델 파일 없음: {self.MODEL_PATH}")

        # 2. 데이터 로딩
        self.teams_master = self._load_teams(self.DATA_DIR)
        
        # 3. N2V 모델 구축
        if self.teams_master:
            self.n2v_model = self._build_n2v_model(self.teams_master)
        else:
            print("❌ 팀 데이터를 찾을 수 없습니다.")

    def _load_teams(self, path):
        teams = []
        if not os.path.exists(path):
            print(f"❌ 경로 오류: '{path}'")
            return teams
        for root, dirs, files in os.walk(path):
            for filename in files:
                if filename.endswith('.json'):
                    try:
                        with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            # Handle list wrapper if present
                            if isinstance(data, list): data = data[0]
                            
                            # Normalize data keys
                            data['team_name'] = data.get('team_name', data.get('team_name_unique', filename.replace('.json', '')))
                            data['team_name_unique'] = data['team_name'] # Keep for compatibility
                            data['league'] = data.get('league', '').upper()
                            data['sport'] = data.get('sport', '')
                            
                            if 'scores' in data:
                                # Remove colons if present
                                data['scores'] = {k.strip().replace(':', ''): v for k, v in data['scores'].items()}
                            
                            teams.append(data)
                    except Exception as e:
                        print(f"Error reading {filename}: {e}")
        return teams

    def _build_n2v_model(self, teams_data):
        print("🚀 N2V 모델 구축 중...")
        G = nx.Graph()
        
        # Add nodes
        for t in teams_data:
            if 'team_name' in t: G.add_node(t['team_name'])
        
        # Add edges based on tag similarity
        for i in range(len(teams_data)):
            for j in range(i + 1, len(teams_data)):
                tags1 = set(teams_data[i].get('style_tags', []))
                tags2 = set(teams_data[j].get('style_tags', []))
                common = len(tags1.intersection(tags2))
                if common > 0:
                    G.add_edge(teams_data[i]['team_name'], teams_data[j]['team_name'], weight=common)
        
        if len(G.nodes) < 2: return None
        
        n2v = Node2Vec(G, dimensions=64, walk_length=10, num_walks=40, workers=1, quiet=True)
        return n2v.fit(window=5, min_count=1)

    def calculate_integrated_score(self, query, anchor_name, candidate):
        """
        Calculate individual scores for a single candidate team against a user query and anchor team.
        Returns:
            weighted_total_score, s_sem, s_rel, s_vec
        """
        # 1. Semantic Score (SBERT)
        cand_tags = " ".join(candidate.get('style_tags', []))
        if self.model_nlp:
            embs = self.model_nlp.encode([query, cand_tags])
            s_sem = cosine_similarity([embs[0]], [embs[1]])[0][0]
        else:
            s_sem = 0

        # 2. Relational Score (Node2Vec)
        s_rel = 0.5
        if self.n2v_model and anchor_name and anchor_name != "None":
             # Check if both in vocab
            if anchor_name in self.n2v_model.wv and candidate['team_name'] in self.n2v_model.wv:
                 s_rel = self.n2v_model.wv.similarity(anchor_name, candidate['team_name'])

        # 3. Vector Score (Weighted)
        ts = candidate.get('scores', {})
        metrics = ['strength', 'money', 'star_power', 'attack_style', 'underdog_feel', 'fan_passion', 'tradition']
        t_vec = np.array([ts.get(m, 10) for m in metrics])
        
        # League weights logic from 03.py
        cand_league = candidate.get('league', '').upper()
        l_weight = np.array([1.0]*7)
        if 'F1' in cand_league: 
            l_weight = np.array([1.5, 1.5, 1.3, 1.0, 1.0, 0.7, 0.5])
        elif 'EPL' in cand_league: 
            l_weight = np.array([1.3, 1.2, 1.1, 1.4, 1.0, 1.0, 1.0])
        elif 'KBO' in cand_league or 'K LEAGUE' in cand_league: 
            l_weight = np.array([1.0, 0.8, 1.0, 1.0, 1.2, 1.5, 1.5])
        
        weighted_t_vec = t_vec * l_weight
        
        target_vec = np.array([10]*7)
        s_multiplier = 1.0

        # Scenario Logic (Keywords)
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
            
        s_vec = cosine_similarity(target_vec.reshape(1, -1), weighted_t_vec.reshape(1, -1))[0][0]
        
        # Combined match score
        manual_match_score = (s_sem * self.ALPHA) + (s_rel * self.BETA) + (s_vec * self.GAMMA)
        manual_match_score *= s_multiplier
        
        return manual_match_score, s_sem, s_rel, s_vec

    def recommend(self, query, user_type, support_team, target_league):
        """
        Main recommendation logic.
        1. Identify candidates in target league.
        2. Calculate component scores (SBERT, Node2Vec, Rule-based Vector).
        3. Predict final score using ML model.
        4. Return top team + metadata.
        """
        json_league_name = self.LEAGUE_MAP.get(target_league, target_league)
        
        candidates = [t for t in self.teams_master if t.get('league', '').lower() == json_league_name.lower()]
        if not candidates:
            return {"error": f"'{target_league}'에 해당하는 팀을 찾을 수 없습니다."}

        # PCA Transform for Model Input
        if self.pca and self.model_nlp:
            query_pca = self.pca.transform(self.model_nlp.encode([query]))[0]
        else:
            query_pca = np.zeros(5) 

        pca_cols = ['의도_팬덤정체성', '의도_스타성과강함', '의도_명문과기적', '의도_비주얼과매력', '의도_자본과지배력']

        rows = []
        for cand in candidates:
            score, s_sem, s_rel, s_vec = self.calculate_integrated_score(query, support_team, cand)
            
            row = {
                'matching_team': cand['team_name'],
                'user_type': int(user_type),
                'recommend_league': json_league_name,
                'sbert_score': s_sem,
                'n2v_score': s_rel,
                'vector_score': s_vec,
                'manual_match_score': score,
                'team_data': cand 
            }
            for i, col in enumerate(pca_cols): row[col] = query_pca[i]
            rows.append(row)

        df_inf = pd.DataFrame(rows)
        
        if self.le_league:
            df_inf['recommend_league_enc'] = self.le_league.transform(df_inf['recommend_league'].astype(str))
        else:
             df_inf['recommend_league_enc'] = 0 # Fallback
        
        if self.scaler:
            score_cols = ['sbert_score', 'n2v_score', 'vector_score']
            scaled = self.scaler.transform(df_inf[score_cols])
            df_inf['sbert_score_mm'], df_inf['n2v_score_mm'], df_inf['vector_score_mm'] = scaled[:,0], scaled[:,1], scaled[:,2]
        else:
             # Fallback if scaler missing
             df_inf['sbert_score_mm'] = df_inf['sbert_score']
             df_inf['n2v_score_mm'] = df_inf['n2v_score']
             df_inf['vector_score_mm'] = df_inf['vector_score']

        if self.final_model and self.input_features:
            # Ensure columns exist
            X_input = df_inf.copy()
            
            # Missing columns fill with 0
            for col in self.input_features:
                if col not in X_input.columns:
                    X_input[col] = 0
            
            X_input = X_input[self.input_features]
            
            cat_cols = [c for c in ["user_type", "recommend_league_enc"] if c in self.input_features]
            for c in cat_cols: X_input[c] = X_input[c].astype('category')
            
            df_inf['predict_score'] = self.final_model.predict(X_input)
        else:
            df_inf['predict_score'] = 0

        # Hybrid Score
        df_inf['final_hybrid_score'] = (df_inf['manual_match_score'] * 0.8) + (df_inf['predict_score'] * 0.2)
        
        # Sort
        df_result = df_inf.sort_values(by='final_hybrid_score', ascending=False)
        
        # Return top result
        if df_result.empty:
             return {"error": "No recommendations available."}

        top_team = df_result.iloc[0]
        
        # Top 2, 3
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
            "others": others
        }
