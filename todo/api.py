from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_crudrouter import SQLAlchemyCRUDRouter as CRUDRouter
from sqlmodel import create_engine
from starlette_admin.contrib.sqla import Admin, ModelView

from db import DATABASE_URL, get_db
from models import Item, ItemCreate, ItemUpdate

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
        schema=Item,
        create_schema=ItemCreate,
        update_schema=ItemUpdate,
        db_model=Item,
        db=get_db,
    ),
    prefix="/api",
)

# Create admin
ENGINE = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
admin = Admin(ENGINE, title="Example: SQLAlchemy")

# Add view
admin.add_view(ModelView(Item))

# Mount admin to your app
admin.mount_to(app)


@app.get("/")
def read_root():
    return {"status": "OK"}
