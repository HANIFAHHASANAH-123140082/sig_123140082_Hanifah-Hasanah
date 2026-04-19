from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

# Auth Schemas
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    @validator('username')
    def username_min_length(cls, v):
        if len(v) < 3:
            raise ValueError('Username minimal 3 karakter')
        return v

    @validator('password')
    def password_min_length(cls, v):
        if len(v) < 6:
            raise ValueError('Password minimal 6 karakter')
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Fasilitas Schemas
class FasilitasCreate(BaseModel):
    nama: str
    jenis: str
    alamat: str
    latitude: float
    longitude: float
    deskripsi: Optional[str] = None

    @validator('nama')
    def nama_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Nama tidak boleh kosong')
        return v

    @validator('latitude')
    def lat_valid(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError('Latitude harus antara -90 dan 90')
        return v

    @validator('longitude')
    def lon_valid(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError('Longitude harus antara -180 dan 180')
        return v

class FasilitasUpdate(FasilitasCreate):
    pass

class FasilitasResponse(BaseModel):
    id: int
    nama: str
    jenis: str
    alamat: str
    latitude: float
    longitude: float
    deskripsi: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True