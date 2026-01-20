from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database.extensions import db
import datetime

# ✅ User 모델 정의 (MySQL 'users_info' 테이블과 매핑)
class User(UserMixin, db.Model):
    # 테이블 이름을 'users_info'로 명시적으로 지정
    __tablename__ = 'users_info' 

    # 스키마 요구사항: user_id(PK), id(Login ID), pwd, email, name, created_date
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True) # 고유 번호 (PK)
    id = db.Column(db.String(50), unique=True, nullable=False) # 로그인 아이디
    pwd = db.Column(db.String(256), nullable=False) # 암호화된 비밀번호
    email = db.Column(db.String(120), unique=True, nullable=False) # 이메일
    name = db.Column(db.String(100), nullable=False) # 사용자 이름
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow) # 가입일

    # 비밀번호 설정 함수 (입력받은 비밀번호를 암호화하여 저장)
    def set_password(self, password):
        self.pwd = generate_password_hash(password)

    # 비밀번호 확인 함수 (입력받은 비밀번호와 저장된 암호화 비밀번호 비교)
    def check_password(self, password):
        return check_password_hash(self.pwd, password)
    
    # Flask-Login용 get_id override (로그인 ID인 'id' 컬럼을 세션 키로 사용)
    def get_id(self):
        return self.id

# ✅ Team 모델 정의 (MySQL 'team_info' 테이블과 매핑)
class Team(db.Model):
    __tablename__ = 'team_info'
    
    # 추정되는 스키마: team_id(PK), team_name, ...
    team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String(100), unique=True, nullable=False)
    sport = db.Column(db.String(50))
    league = db.Column(db.String(50))
    # 필요한 컬럼만 정의

# ✅ ChatLog 모델 정의 (MySQL 'chat_logs' 테이블과 매핑)
class ChatLog(db.Model):
    __tablename__ = 'chat_logs'

    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False) # users_info.user_id (참조 설정은 선택)
    input_query = db.Column(db.String(100), nullable=False)
    favorite_team_id = db.Column(db.Integer, nullable=True) # team_info.team_id
    recommended_team_id = db.Column(db.JSON, nullable=False) # Top 3 Team IDs {"1": id, "2": id, "3": id}
    recommendation_score = db.Column(db.Integer, nullable=False)
    is_liked = db.Column(db.Boolean, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
