from sqlalchemy import create_engine, Column, String, Integer, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid
from config import DATABASE_URL

# Database setup
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class VideoJob(Base):
    """Model for tracking video generation jobs"""
    
    __tablename__ = "video_jobs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    idea = Column(Text, nullable=False)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    script = Column(Text, nullable=True)
    
    # Status tracking
    status = Column(String(50), default="queued")  # queued, processing, completed, failed
    progress = Column(Integer, default=0)  # 0-100
    
    # Generation details
    video_url = Column(String(500), nullable=True)
    video_path = Column(String(500), nullable=True)
    thumbnail_url = Column(String(500), nullable=True)
    
    # Upload details
    platforms = Column(JSON, default=list)
    upload_links = Column(JSON, nullable=True)
    
    # Metadata
    tags = Column(JSON, default=list)
    hashtags = Column(JSON, default=list)
    
    # Error tracking
    error = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime, nullable=True)
    
    # Engagement metrics (after upload)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    
    @classmethod
    def create(cls, **kwargs):
        """Create new video job"""
        job = cls(**kwargs)
        db = SessionLocal()
        db.add(job)
        db.commit()
        db.refresh(job)
        return job
    
    @classmethod
    def get_by_id(cls, job_id: str):
        """Get job by ID"""
        db = SessionLocal()
        return db.query(cls).filter(cls.id == job_id).first()
    
    @classmethod
    def get_all(cls, limit: int = 20, offset: int = 0):
        """Get all jobs with pagination"""
        db = SessionLocal()
        return db.query(cls).limit(limit).offset(offset).all()
    
    def save(self):
        """Save changes"""
        db = SessionLocal()
        db.merge(self)
        db.commit()
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "idea": self.idea,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "progress": self.progress,
            "video_url": self.video_url,
            "platforms": self.platforms,
            "upload_links": self.upload_links,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "views": self.views,
            "likes": self.likes,
            "shares": self.shares
        }


# Create tables
Base.metadata.create_all(bind=engine)
