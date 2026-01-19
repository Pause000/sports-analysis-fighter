from app import app, db, User
import os
import sys

# MySQL 연결 테스트 스크립트
# 실제 DB에 접속하여 테이블을 생성하고 간단한 데이터를 넣어봅니다.

def test_mysql_connection():
    print("🚀 MySQL 연결 테스트 시작...")
    
    try:
        with app.app_context():
            # DB 연결 정보 확인
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            if 'mysql' not in db_uri:
                print("❌ 경고: 현재 설정이 MySQL이 아닙니다!")
                print(f"현재 URI: {db_uri}")
                return

            # 기존 테이블 삭제 (스키마 변경 적용을 위해)
            # 주의: 데이터가 모두 날아갑니다!
            print("⚠️ 기존 'users_info' 및 'user_info' 정리 중...")
            
            # 과거 테이블명이 있다면 삭제 시도 (클린업)
            try:
                db.session.execute(db.text("DROP TABLE IF EXISTS user_info"))
                db.session.execute(db.text("DROP TABLE IF EXISTS users_info"))
                db.session.commit()
            except Exception as e:
                print(f"테이블 삭제 중 경고 (무시 가능): {e}")

            print("✅ 기존 테이블 삭제 완료")

            # 테이블 생성
            print("🛠 'users_info' 테이블 생성 시도...")
            db.create_all()
            print("✅ 테이블 생성 완료")

            # 테스트 유저 생성
            test_login_id = "testuser"
            print(f"🆕 새 테스트 유저 생성 중: {test_login_id}")
            
            # 모델 변경에 맞춘 데이터 생성
            new_user = User(
                id=test_login_id,
                pwd="testpassword",  
                email="test@example.com",
                name="테스터"
            )
            
            if hasattr(new_user, 'set_password'):
                new_user.set_password("testpassword123")
            
            db.session.add(new_user)
            db.session.commit()
            print(f"✅ 테스트 유저 저장 완료 (PK: {new_user.user_id}, ID: {new_user.id})")
            
            # 최종 확인
            saved_user = User.query.filter_by(id=test_login_id).first()
            if saved_user:
                print(f"🎉 MySQL 연결 및 읽기/쓰기 테스트 최종 성공! (테이블: {User.__tablename__}, 가입일: {saved_user.created_date})")
            else:
                print("❌ 유저 저장 후 조회 실패")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_mysql_connection()
