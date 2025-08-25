from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="EHS Safety Portal")

# Allow frontend (Vercel) to connect
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "https://ehs-portal.vercel.app",  # replace with your actual Vercel link later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def health_check():
    return {"ok": True}
