from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI()

# CORS 허용 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 클라이언트에서 전송할 시청 로그 데이터 구조
class WatchLogSchema(BaseModel):
    videoId: str
    userId: Optional[str] = "guest_user"
    lastPosition: float
    isCompleted: bool
    currentQuality: str

@app.post("/api/watch-log")
async def collect_watch_log(log: WatchLogSchema):
    # 실제 실무 환경에서는 이 로그를 DB(PostgreSQL, MongoDB)나 Kafka로 전송
    print(f"📥 [Log Received] User: {log.userId} | Video: {log.videoId} | "
          f"Pos: {log.lastPosition}s | Quality: {log.currentQuality} | Completed: {log.isCompleted}")
    
    return {"status": "success", "message": "Log recorded"}

@app.get("/")
async def get_index():
    return FileResponse("index.html")

app.mount("/", StaticFiles(directory="."), name="static")