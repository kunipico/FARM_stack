from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import route_todo, route_auth
from schemas import SuccessMsg, CsrfSettings
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError


app = FastAPI()
app.include_router(route_todo.router)
app.include_router(route_auth.router)
# 2024.02.17 デプロイ先をAWSに変更する作業を行っている。
# フロント部分をFire base　→　S3に変更
# CORSエラーが発生、オリジンにS3アドレスを追加
origins = ['http://localhost:3000', 'https://udemy-lesson-farm-stack-app.web.app', 'http://farm-react-todo.s3-website-ap-northeast-1.amazonaws.com/']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail':  exc.message
                 }
    )


@app.get("/", response_model=SuccessMsg)
def root():
    return {"message": "Welcome to FastAPI."}

