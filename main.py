from fastapi import FastAPI
import user_router
app = FastAPI()

app.include_router(user_router.router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
