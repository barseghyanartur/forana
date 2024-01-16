from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_crudrouter import SQLAlchemyCRUDRouter as CRUDRouter
from sqlmodel import create_engine
from starlette_admin.contrib.sqla import Admin, ModelView

from db import DATABASE_URL, get_db
from models import Movie, MovieCreate, MovieUpdate

__all__ = ("app",)


app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    debug=True,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose 'Content-Disposition' header
    expose_headers=["Content-Disposition"],
)

app.include_router(
    CRUDRouter(
        schema=Movie,
        create_schema=MovieCreate,
        update_schema=MovieUpdate,
        db_model=Movie,
        db=get_db,
    ),
    prefix="/api",
)

# Create admin
ENGINE = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
admin = Admin(ENGINE, title="Admin")

# Add view
admin.add_view(ModelView(Movie))

# Mount admin to your app
admin.mount_to(app)


@app.get("/")
def read_root():
    return {"status": "OK"}
