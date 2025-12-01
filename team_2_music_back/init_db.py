"""
SQLite 데이터베이스 초기화 스크립트
모든 테이블을 생성합니다.
"""
from app.db.database import engine, Base
from app.models import models

def init_db():
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    
    # 테이블 목록 출력
    print("\nCreated tables:")
    for table in Base.metadata.sorted_tables:
        print(f"  - {table.name}")

if __name__ == "__main__":
    init_db()
