# 🌤️ Weather Chat App

A full-stack weather assistant app that allows users to:

- Ask real-time weather questions via chat using an LLM (Mistral).
- Create, read, and manage historical weather queries stored in a PostgreSQL database.
- View a list of all stored queries via a clean UI.

---

## 🧰 Tech Stack

- **Frontend:** React.js + Axios + TailwindCSS
- **Backend:** FastAPI + SQLAlchemy
- **Database:** PostgreSQL
- **AI/LLM Integration:** LangChain + Mistral API
- **Weather API:** World Weather Online (or any you choose)

---

## 📦 Project Structure


├── main.py # FastAPI server
├── models.py # SQLAlchemy models
├── database.py # DB connection setup
└── keys.py # API keys and URLs
├── frontend/
│ ├── src/
│ │ ├── App.jsx # React App
│ │ └── index.css # Styles
├── README.md # You're here!


---

## 🚀 Getting Started

### ⚙️ 1. Backend Setup

```bash
pip install -r requirements.txt

# keys.py
WEATHER_API_URL = "https://api.worldweatheronline.com/premium/v1/weather.ashx"
WEATHER_API = "<your-weather-api-key>"

uvicorn main:app --reload

2. Frontend Setup
bash
Copy
Edit
cd frontend
npm install
npm run dev  # or npm start

🔧 Key Features
✅ Chat Functionality (/response)
Integrates LangChain + Mistral to understand and extract weather queries.

Returns real-time weather using coordinates via weather API.

✅ CRUD API Endpoints
POST /create/ – Add a weather query with location, date, session ID, and response.

GET /read/ – View all saved weather queries.

(You can add PUT and DELETE too for full CRUD!)

Make sure you change postgres sql database username and password and create database in postgresql

CREATE DATABASE weatherdb;



![image](https://github.com/user-attachments/assets/3e234158-7a26-4bdb-8e3b-088f6e5997fe)

![image](https://github.com/user-attachments/assets/fa61e1c8-e7f4-4fda-9b0f-e1ffcf9dd685)

