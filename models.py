from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "sqlite:///./test.db"

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    favorite_stories = relationship("FavoriteStory", back_populates="user", cascade="all, delete-orphan")
    saved_stories = relationship("Story", back_populates="user", cascade="all, delete-orphan")

class Story(Base):
    __tablename__ = 'story'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)
    protagonist_name = Column(String)
    protagonist_gender = Column(String)
    friend_name = Column(String)
    friend_gender = Column(String)
    story_theme = Column(String)
    age_group = Column(String)
    educational_content = Column(String)
    story_description = Column(String)
    story_length = Column(String)

    user = relationship("User", back_populates="saved_stories")

class FavoriteStory(Base):
    __tablename__ = 'favorite_story'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    story_content = Column(String)
    summary_text = Column(String)
    bullet_points = Column(String)

    user = relationship("User", back_populates="favorite_stories")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
