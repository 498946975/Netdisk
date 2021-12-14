import uvicorn
from fastapi import FastAPI
from db.db import Base, Engine
from apps.login.views import router as login_router
from apps.user.views import router as user_router
from apps.department.views import router as department_router

# 创建数据库表结构
Base.metadata.create_all(bind=Engine)

app = FastAPI(
    title="fastapi_test",
    description="fastapi_test"
)

app.include_router(login_router)
app.include_router(user_router)
app.include_router(department_router)

if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True, host="127.0.0.1", port=8080)
