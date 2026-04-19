# WebGIS Fasilitas Publik - Kota Bengkulu
Praktikum 9 - Sistem Informasi Geografis

## Fitur
- 🔐 Autentikasi JWT (Register & Login)
- 🗺️ Peta interaktif dengan Leaflet.js
- ➕ CRUD Fasilitas Publik
- 📍 Klik peta untuk pilih koordinat

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy, SQLite, python-jose
- **Frontend**: HTML, CSS, JavaScript, Leaflet.js

## Setup Backend
cd backend
python -m venv venv
venv\Scripts\activate     # Windows
pip install -r requirements.txt
uvicorn main:app --reload

## Setup Frontend
Buka index.html dengan Live Server di VS Code

## API Docs
http://localhost:8000/docs