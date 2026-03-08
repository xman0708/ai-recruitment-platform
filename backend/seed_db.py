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
        
        c1 = Candidate(name="李晓明", job_id=1, status=ProcessStatusEnum.SCREENING, ai_score=92, ai_reasoning="匹配度高", experience="5年", education="本科")
        c2 = Candidate(name="王梦琪", job_id=2, status=ProcessStatusEnum.INTERVIEW, ai_score=88, ai_reasoning="匹配", experience="8年", education="博士")
        c3 = Candidate(name="张三", job_id=1, status=ProcessStatusEnum.NEW, experience="3年", education="硕士")
        db.add_all([c1, c2, c3])
        db.commit()
        
        from models.domain import Interview, InterviewStatusEnum
        i1 = Interview(candidate_id=c1.id, interviewer_id=admin.id, type="视频面试", scheduled_time="今天 14:00 - 15:00", location_or_link="https://meeting.tencent.com/p/123456789", status=InterviewStatusEnum.SCHEDULED)
        i2 = Interview(candidate_id=c2.id, interviewer_id=admin.id, type="线下面试", scheduled_time="昨天 16:00 - 17:00", location_or_link="总部大楼 A 座 302 会议室", status=InterviewStatusEnum.COMPLETED, feedback_score=4, feedback_content="技术非常扎实", recommendation="HIRE")
        db.add_all([i1, i2])
        db.commit()
        print("Done.")
    else:
        print("Database already seeded.")
        
if __name__ == "__main__":
    seed_db()
