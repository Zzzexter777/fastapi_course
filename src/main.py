from fastapi import FastAPI
from api import main_router
import uvicorn

app = FastAPI()

app.include_router(main_router)


@app.get("/")
async def home():
    return "Hello!"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
