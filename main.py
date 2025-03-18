from fastapi import FastAPI
from routers import user_router,plans_router

app = FastAPI()

app.include_router(user_router.router)
app.include_router(plans_router.router)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
