from sqlmodel import SQLModel, Field ,create_engine, Session, select
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    item: str = Field(index=True)
    amount: int


postgresql_url = os.getenv("ITEM_DATABASE_URL")
engine = create_engine(postgresql_url)


def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
