
from sqlalchemy import Column, Integer, String, Enum, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import enum

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    user_id = Column(String, unique=True, nullable=False)

class Route(Base):
    __tablename__ = "routes"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    length_km = Column(Float, nullable=False)
    eco_friendly = Column(Boolean, nullable=False)

class EcoPlace(Base):
    __tablename__ = "eco_places"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    description = Column(String, nullable=False)

class Reward(Base):
    __tablename__ = "rewards"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    points_needed = Column(Integer, nullable=False)
    description = Column(String, nullable=False)

class EcoActionType(str, enum.Enum):
    RECYCLING = "recycling"
    REUSABLE_STORES = "reusable_stores"

class EcoAction(Base):
    __tablename__ = "eco_actions"
    id = Column(String, primary_key=True, index=True)
    location = Column(String, nullable=False)
    action_type = Column(Enum(EcoActionType), nullable=False)
    description = Column(String, nullable=False)

class ForumPost(Base):
    __tablename__ = "forum_posts"
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_email = Column(String, ForeignKey("users.email"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    user = relationship("User")