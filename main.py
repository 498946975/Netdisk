import uvicorn
from fastapi import FastAPI
from db.db import Base, Engine
from apps.api.login.views import router as login_router
from apps.api.user.views import router as user_router
from apps.api.department.views import router as department_router
from apps.api.role.role_views import router as role_router
from apps.api.permission.views import router as permission_router
from apps.api.role.users_permissions_views import router as users_permissions_router
from apps.api.docs.views import router as docs_router
from apps.api.shares.views import router as shares_router
from apps.api.download.views import router as download_router
from apps.config.settings import settings

# 创建数据库表结构
Base.metadata.create_all(bind=Engine)

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESC
)



app.include_router(login_router)
app.include_router(user_router)
app.include_router(department_router)
app.include_router(role_router)
app.include_router(permission_router)
app.include_router(users_permissions_router)
app.include_router(docs_router)
app.include_router(shares_router)
app.include_router(download_router)

if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True, host="0.0.0.0", port=8888)
