from fastapi import FastAPI

# orm and config
from . import models
from .database import engine

# routers
from .routers import user, post, auth, vote

# middleware
from fastapi.middleware.cors import CORSMiddleware

# # establish db connection
# since we are using alembic for migrations, we don't need to create the tables here anymore
# models.Base.metadata.create_all(bind=engine) 

# init the app
app = FastAPI()

# middleware
# allowed domain to access the api. wildcard "*" allows everything

origins = [
    "https://www.google.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# include routers
app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def root():
    return {'message': 'Welcome to fastapi!!!'}



