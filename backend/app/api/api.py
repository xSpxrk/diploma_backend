from fastapi import FastAPI, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer

from .endpoints import customers, offers, providers, orders, login, user, reviews, materials
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://bsm-frontend.herokuapp.com/"
]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(login.router, prefix="", tags=["login"])
app.include_router(customers.router, prefix="/customers", tags=["customers"])
app.include_router(offers.router, prefix="/offers", tags=["offers"])
app.include_router(providers.router, prefix="/providers", tags=["providers"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(reviews.router, prefix='/reviews', tags=['reviews'])
app.include_router(materials.router, prefix='/materials', tags=['materials'])
