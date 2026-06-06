from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, worldcup, admin

app = FastAPI(title="SAI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(worldcup.router)
app.include_router(admin.router)

@app.get("/api/health")
def health():
    return {"status": "ok"}
