import bcrypt
if not hasattr(bcrypt, '__about__'):
    bcrypt.__about__ = type('about', (), {'__version__': bcrypt.__version__})()
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas, auth
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="WebGIS Fasilitas Publik API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency: ambil user dari token
def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token tidak ditemukan")
    token = authorization.split(" ")[1]
    username = auth.decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Token tidak valid")
    user = auth.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User tidak ditemukan")
    return user

# ===== AUTH ENDPOINTS =====
@app.post("/auth/register", response_model=schemas.Token)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    if auth.get_user_by_username(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username sudah digunakan")
    user = models.User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=auth.hash_password(user_data.password)
    )
    db.add(user)
    db.commit()
    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/auth/login", response_model=schemas.Token)
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Username atau password salah")
    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# ===== FASILITAS ENDPOINTS (CRUD) =====
@app.get("/fasilitas", response_model=List[schemas.FasilitasResponse])
def get_all_fasilitas(db: Session = Depends(get_db)):
    return db.query(models.Fasilitas).all()

@app.post("/fasilitas", response_model=schemas.FasilitasResponse)
def create_fasilitas(
    data: schemas.FasilitasCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    fasilitas = models.Fasilitas(**data.dict())
    db.add(fasilitas)
    db.commit()
    db.refresh(fasilitas)
    return fasilitas

@app.get("/fasilitas/{id}", response_model=schemas.FasilitasResponse)
def get_fasilitas(id: int, db: Session = Depends(get_db)):
    fasilitas = db.query(models.Fasilitas).filter(models.Fasilitas.id == id).first()
    if not fasilitas:
        raise HTTPException(status_code=404, detail="Fasilitas tidak ditemukan")
    return fasilitas

@app.put("/fasilitas/{id}", response_model=schemas.FasilitasResponse)
def update_fasilitas(
    id: int,
    data: schemas.FasilitasUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    fasilitas = db.query(models.Fasilitas).filter(models.Fasilitas.id == id).first()
    if not fasilitas:
        raise HTTPException(status_code=404, detail="Fasilitas tidak ditemukan")
    for key, value in data.dict().items():
        setattr(fasilitas, key, value)
    db.commit()
    db.refresh(fasilitas)
    return fasilitas

@app.delete("/fasilitas/{id}")
def delete_fasilitas(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    fasilitas = db.query(models.Fasilitas).filter(models.Fasilitas.id == id).first()
    if not fasilitas:
        raise HTTPException(status_code=404, detail="Fasilitas tidak ditemukan")
    db.delete(fasilitas)
    db.commit()
    return {"message": "Fasilitas berhasil dihapus"}