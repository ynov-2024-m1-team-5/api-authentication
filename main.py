from fastapi import FastAPI
from routes.authentificationRoutes import usersRoutes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# origins = [
#     "http://localhost:3000",
#     "http://localhost:8080",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app = FastAPI(title="authentification")

app.include_router(usersRoutes, prefix="/api/v1")
