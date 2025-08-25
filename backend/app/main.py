from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, users, incidents, actions, reports
from .database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EHS Safety Portal")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "https://ehs-portal.vercel.app",  # replace later with your Vercel link
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(incidents.router)
app.include_router(actions.router)
app.include_router(reports.router)

@app.get("/healthz")
def health_check():
    return {"ok": True}
