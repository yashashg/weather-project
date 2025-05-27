# from keys import WEATHER_API_URL,WEATHER_API,LANGSMITH_API_KEY,LANGSMITH_PROJECT,MISTRAL_API_KEY
from keys import WEATHER_API_URL,WEATHER_API
from langchain.chat_models import init_chat_model
from typing_extensions import Annotated, TypedDict
import requests
from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, SystemMessage
from database import SessionLocal
from models import WeatherQuery
from sqlalchemy.orm import Session
from datetime import date

origins = [
    "http://localhost:3000",  # React frontend
    # Add other domains here for production
]
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


model = init_chat_model("mistral-large-latest", model_provider="mistralai")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],              # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],              # Allow all headers
)
class extract_location(TypedDict):
    """Extract structured location data from the input"""

    # Annotations must have the type and can optionally include a default value and description (in that order).
    city: Annotated[str, ..., "City"]
    country: Annotated[str, ..., "country"]
    longitude: Annotated[str, ..., "longitude of the city"]
    latitude: Annotated[str, ..., "latitude of the city"]

def weather(latitude,longitude):
    params = {
        "q": f"{latitude},{longitude}",
        "key": WEATHER_API,
        "units": "metric",
        
    }
    response = requests.get(WEATHER_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    return {"error": f"Failed to retrieve weather data {response.status_code}" } 

class query(BaseModel):
    query: str


tools = [extract_location]
llm_with_tools = model.bind_tools(tools)


@app.post("/response/")
def ai(query: query):
    query = query.query
    if not query:
        return {"error": "Missing 'query' field"}, 400
    messages = [
        SystemMessage("You are a professional real time weather forecast reporter, dont provide any mock data provide only the gicen data in function call. Give the latest weather report for [City, Country] in a clear, concise tone. Include temperature, humidity, and any alerts and the forecast for the next 2-3 days. End with a short suggestion or tip for the day (e.g., carry an umbrella, stay hydrated). Keep the report under 100 words. Your answer should be plain text no text decoration or formatting."),
        HumanMessage(query),
    ]
    response =llm_with_tools.invoke(query).tool_calls
    if "error" in response:
        return {"error": response["error"]}, 500
    
    if response == []:
        return model.invoke(messages).content
    
    latitude= response[0]["args"].get("latitude")
    longitude= response[0]["args"].get("longitude")
    details = weather(latitude,longitude)
    # messages.append(response) 
    messages.append(HumanMessage(str([details["forecast"]["forecastday"][0]["day"]])))
    return model.invoke(messages).content

@app.post("/create/")
def save_query(location: str,date_queried:date,session_id: str,  response: str, db: Session = Depends(get_db)):
    entry = WeatherQuery(session_id=session_id, location=location, date_queried =date_queried,response=response)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@app.get("/read/")
def get_queries(db: Session = Depends(get_db)):
    return db.query(WeatherQuery).all()


