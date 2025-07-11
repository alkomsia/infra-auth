from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
import casbin
from casbin_sqlalchemy_adapter import Adapter
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Инициализация Casbin Enforcer
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logging.error("DATABASE_URL not set in environment variables.")
    raise RuntimeError("DATABASE_URL not configured")

try:
    adapter = Adapter(DATABASE_URL)
    enforcer = casbin.Enforcer("app/model.conf", adapter)
    logging.info("Casbin Enforcer initialized successfully")
except Exception as e:
    logging.exception("Failed to initialize Casbin Enforcer")
    raise

# Middleware для авторизации
@app.middleware("http")
async def authorize(request: Request, call_next):
    # Извлекаем информацию о пользователе и ресурсе
    sub = request.headers.get("X-User", "anonymous")  # Используйте заголовок или сессию для извлечения пользователя
    obj = request.url.path
    act = request.method

    # Проверяем наличие правила в Casbin
    if not enforcer.enforce(sub, obj, act):
        logging.warning(f"No rule found for user '{sub}' on {act} {obj}")
        # Если правило не найдено, возвращаем отказ в доступе
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Access Denied"}
        )

    # Если правило найдено, продолжаем выполнение запроса
    response = await call_next(request)
    return response

# Примерные endpoints
@app.get("/dashboard")
def dashboard():
    return {"message": "Welcome to the dashboard!"}

@app.post("/settings")
def update_settings():
    return {"message": "Settings updated"}

@app.get("/")
def index():
    return {"message": "Welcome"}

# Обработчик непредвиденных ошибок
@app.exception_handler(Exception)
async def internal_server_error(request: Request, exc: Exception):
    logging.error(f"Unexpected error occurred: {exc}")
    return JSONResponse(status_code=500, content={"message": "Internal Server Error", "error": str(exc)})

