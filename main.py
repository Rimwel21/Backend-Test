from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.accounts_route import router as account_auth
from routes.refresh_token import router as refresh_router

app = FastAPI()

# origins = [] lalagyan kopa, kung sino lang pwede maka access pag frontend

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # babaguhin koto kapag may frontend na
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(account_auth)
app.include_router(refresh_router)

@app.get("/")
def root():
    return{"message": "FastAPI running on Port 8000..."}