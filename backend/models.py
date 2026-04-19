from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Fasilitas(Base):
    __tablename__ = "fasilitas"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    jenis = Column(String, nullable=False)
    alamat = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    deskripsi = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())