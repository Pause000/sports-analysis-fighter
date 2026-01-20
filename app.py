# =========================================================
# 1. Imports & Configuration
# =========================================================
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Data Processing & ML Libraries
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

# Environment Variables
from dotenv import load_dotenv
load_dotenv()

warnings.filterwarnings("ignore")

# Initialize Flask App
app = Flask(__name__, static_folder='web/static', template_folder='web/templates')

# =========================================================
# 2. Database & Login Setup
# =========================================================

# MySQL 데이터베이스 연결 설정 (database/scripts/connection.py 사용)
from database.scripts.connection import get_db_uri

app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()

# 보안을 위한 비밀 키 설정 (세션 관리 등에 사용)
app.config['SECRET_KEY'] = 'dev-secret-key-1234' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 불필요한 이벤트 추적 비활성화 (성능 향상)

# ✅ DB & Login Manager 초기화
from database.extensions import db
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # 로그인이 안 된 유저가 접근하면 'login' 라우트로 리다이렉트

# ✅ 모델 import (db 초기화 후)
from database.models import User, Team, ChatLog
import datetime


# Load User for Login Manager
@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login helper to retrieve a user from our db.
    """
    return User.query.filter_by(id=user_id).first()

# =========================================================
# 3. Recommendation Engine Initialization
# =========================================================
from scripts.recommendation_engine import RecommendationEngine
import uuid

# Initialize Recommendation Engine
# (Manages NLP models, Node2Vec, and Artifacts internally)
rec_engine = RecommendationEngine(data_dir='./database/JSON', model_path='./fit_model.joblib')

# =========================================================
# 4. Flask Routes
# =========================================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    try:
        # 폼 데이터 또는 JSON 데이터 처리
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        user_id = data.get('id')
        password = data.get('pwd') # HTML form name='pwd' 가정
        email = data.get('email')
        name = data.get('name')

        if not user_id or not password:
            return jsonify({"error": "아이디와 비밀번호는 필수입니다."}), 400

        # 중복 체크
        if User.query.filter_by(id=user_id).first():
             return jsonify({"error": "이미 존재하는 아이디입니다."}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "이미 존재하는 이메일입니다."}), 400

        # user_id(PK)는 자동생성되므로 id(로그인 아이디)만 넘겨줌
        new_user = User(id=user_id, email=email, name=name)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        
        # 폼 요청이면 리다이렉트, JSON 요청이면 JSON 응답
        if not request.is_json:
            return render_template('index.html', user=new_user)
            
        return jsonify({"message": "회원가입 성공", "user": {"id": user_id, "name": name}})
    except Exception as e:
        print(f"Register Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    try:
        if request.is_json:
            data = request.get_json()
            user_id = data.get('id')
            password = data.get('pwd')
        else:
            user_id = request.form.get('id') # Form data
            password = request.form.get('pwd')

        user = User.query.filter_by(id=user_id).first()

        if user and user.check_password(password):
            login_user(user)
            
            if not request.is_json:
                 return render_template('index.html', user=user)

            return jsonify({"message": "로그인 성공", "user": {"id": user.id, "name": user.name}})
        
        if not request.is_json:
            return render_template('login.html', error="아이디 또는 비밀번호가 올바르지 않습니다.")

        return jsonify({"error": "아이디 또는 비밀번호가 올바르지 않습니다."}), 401
    except Exception as e:
        print(f"Login Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/logout', methods=['GET', 'POST']) # GET도 허용 (링크로 로그아웃 시)
@login_required
def logout():
    logout_user()
    if not request.is_json:
        return render_template('index.html', user=None)
    return jsonify({"message": "로그아웃 성공"})

@app.route('/api/status')
def auth_status():
    if current_user.is_authenticated:
        return jsonify({"is_authenticated": True, "user": {"email": current_user.email, "name": current_user.name}})
    else:
        return jsonify({"is_authenticated": False})

@app.before_request
def startup():
    if rec_engine.final_model is None:
        rec_engine.load_resources()

@app.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)

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
        result = rec_engine.recommend(
            query=query,
            user_type=user_type,
            support_team=support_team,
            target_league=league
        )

        if "error" in result:
            return jsonify(result), 404
        
        # ---------------------------------------------------------
        # ✅ DB 로그 저장 (로그인 사용자만)
        if current_user.is_authenticated:
            try:
                # 1. 추천된 팀 Names 수집 (Top 1 + Others)
                top_team_name = result.get("team_name")
                other_teams = result.get("others", [])
                
                # 순서대로 이름 리스트 생성
                ranked_names = [top_team_name] + [o['name'] for o in other_teams]
                
                # 2. 팀 ID 조회 (한 번에 조회)
                teams_obj = Team.query.filter(Team.team_name.in_(ranked_names)).all()
                name_to_id = {t.team_name: t.team_id for t in teams_obj}
                
                # [DEBUG]
                missing_names = set(ranked_names) - set(name_to_id.keys())
                if missing_names:
                    print(f"⚠️ [Log Warning] Missing matched teams in DB: {missing_names}")
                    print(f"   - Ranked: {ranked_names}")
                    print(f"   - Found: {list(name_to_id.keys())}")

                # 3. JSON 데이터 생성 {"1": id, "2": id, "3": id}
                rec_team_json = {}
                for i, name in enumerate(ranked_names):
                    if name in name_to_id:
                        rec_team_json[str(i+1)] = name_to_id[name]
                    else:
                        print(f"   -> Skipping rank {i+1} ({name}) - ID not found")
                
                # (1위 팀 ID는 별도로 필요하지 않으면 JSON에만 저장. 기존 로직 호환 위해 1위 ID를 찾긴 해야할 수도 있지만, 스키마가 변경되었으므로 JSON 필드에 저장)

                # 4. 선호 팀 ID 조회 (있다면)
                fav_team_id = None
                if support_team and isinstance(support_team, dict):
                    fav_name = support_team.get("team_name")
                    if fav_name:
                        fav_obj = Team.query.filter_by(team_name=fav_name).first()
                        if fav_obj:
                             fav_team_id = fav_obj.team_id
                
                # 5. Input Query (모델에 들어간 최종 쿼리)
                
                # 6. 로그 저장
                new_log = ChatLog(
                    user_id=current_user.user_id,
                    input_query=query,
                    favorite_team_id=fav_team_id,
                    recommended_team_id=rec_team_json, # JSON 저장
                    recommendation_score=int(result.get("match_percent", 0)),
                    is_liked=None 
                )
                db.session.add(new_log)
                db.session.commit()
                print(f"✅ Chat Log Saved: User={current_user.user_id}, Teams={rec_team_json}")
                
                # 결과에 log_id 추가
                result['log_id'] = new_log.log_id

            except Exception as log_e:
                print(f"❌ Chat Log Error: {log_e}")
                db.session.rollback()
        # ---------------------------------------------------------

        return jsonify(result)

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
@login_required
def feedback():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    log_id = data.get('log_id')
    is_liked = data.get('is_liked') # true or false

    if log_id is None or is_liked is None:
        return jsonify({"error": "Missing log_id or is_liked"}), 400

    try:
        log_entry = ChatLog.query.filter_by(log_id=log_id, user_id=current_user.user_id).first()
        if not log_entry:
            return jsonify({"error": "Log not found or unauthorized"}), 404

        log_entry.is_liked = bool(is_liked)
        db.session.commit()
        
        return jsonify({"message": "Feedback saved", "log_id": log_id, "is_liked": log_entry.is_liked})
    except Exception as e:
        db.session.rollback()
        print(f"Feedback Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # 로컬 개발용
    with app.app_context():
        db.create_all()
        print("✅ 데이터베이스 초기화 및 연결 확인 완료 (MySQL user_info 테이블)")
    
    rec_engine.load_resources() # Run immediately for dev
    app.run(host='0.0.0.0', port=5000, debug=True)


