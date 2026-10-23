import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Movie(BaseModel):
    titles: List
    mood: str
    message: str

recommendationDict = {
    "sad": [
        {"title": "The Pursuit of Happiness", "genre": "Drama/Biography"},
        {"title": "Good Will Hunting", "genre": "Drama/Romance"},
        {"title": "The Shawshank Redemption", "genre": "Drama"}
    ],
    "happy": [
        {"title": "Paddington 2", "genre": "Comedy/Family"},
        {"title": "La La Land", "genre": "Musical/Romance"},
        {"title": "The Grand Budapest Hotel", "genre": "Comedy/Crime"}
    ],
    "bored": [
        {"title": "Everything Everywhere All at Once", "genre": "Sci-Fi/Action"},
        {"title": "Knives Out", "genre": "Mystery/Comedy"},
        {"title": "Spider-Man: Into the Spider-Verse", "genre": "Animation/Action"}
    ]
}

@app.get("/movies/recommend", response_model=Movie)
def recommend(mood:str):
    if mood.lower() in recommendationDict:
        titles = [data["title"] for data in recommendationDict[mood]]
        return Movie(titles=titles, mood=mood, message="Here are the recommendations for " + mood)
    else:
        return Movie(titles=[], mood=mood, message="No Movie is available for this mood.")


@app.get("/health/check")
def health_check():
    READY_VARIABLE = os.environ.get("READY_VARIABLE", "ready")
    if READY_VARIABLE != "ready":
        raise HTTPException(status_code=503, detail="Service Unavailable")
    return {"status": "ok"}

