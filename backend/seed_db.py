from database.session import SessionLocal, engine
from models.domain import Base, Job, Candidate, User, JobStatusEnum, ProcessStatusEnum, RoleEnum
from datetime import datetime

def seed_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if empty
    if db.query(Job).count() == 0:
        print("Seeding database...")
        admin = User(username="admin", email="admin@test.com", hashed_password="pwd", role=RoleEnum.HR)
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        job1 = Job(title="高级前端开发工程师（Vue3）", department="研发中心", description="负责招聘平台开发", status=JobStatusEnum.OPEN, created_by=admin.id)
        job2 = Job(title="Python 后端架构师", department="AI 研发部", description="负责 FastAPI 与 LLM 接入", status=JobStatusEnum.OPEN, created_by=admin.id)
        db.add_all([job1, job2])
        db.commit()
        
        c1 = Candidate(name="李晓明", job_id=1, status=ProcessStatusEnum.SCREENING, ai_score=92, ai_reasoning="匹配度高", exp="5年", edu="本科")
        c2 = Candidate(name="王梦琪", job_id=2, status=ProcessStatusEnum.INTERVIEW, ai_score=88, ai_reasoning="匹配", exp="8年", edu="博士")
        c3 = Candidate(name="张三", job_id=1, status=ProcessStatusEnum.NEW, exp="3年", edu="硕士")
        db.add_all([c1, c2, c3])
        db.commit()
        print("Done.")
    else:
        print("Database already seeded.")
        
if __name__ == "__main__":
    seed_db()
