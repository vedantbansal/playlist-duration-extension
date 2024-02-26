from fastapi import FastAPI, Response

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
from youtube_service import yt_service_impl

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/find-duration")
async def hello(playlistId: str):

    yt_service = yt_service_impl(playlistId=playlistId)
    ls = yt_service.calculate_duration()
    return ls