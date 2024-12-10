from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import koriander

app = FastAPI()

# CORSミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では具体的なオリジンを指定することを推奨
    allow_credentials=True,
    allow_methods=["*"],  # 許可するHTTPメソッド
    allow_headers=["*"],  # 許可するHTTPヘッダー
)

app.include_router(koriander.router)
