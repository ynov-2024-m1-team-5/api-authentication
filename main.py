from fastapi import FastAPI
from routes.authentificationRoutes import usersRoutes

app = FastAPI(title="authentification")

app.include_router(usersRoutes, prefix="/api/v1")
