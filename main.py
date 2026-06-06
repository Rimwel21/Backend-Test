from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.accounts_route import router as studentAuth


app = FastAPI()

# origins = [] lalagyan kopa, kung sino lang pwede maka access pag frontend

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(studentAuth)

@app.get("/")
def root():
    return{"message": "FastAPI running on Port 8000..."}