from sqlmodel import SQLModel, Field, create_engine
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()



class Item(SQLModel):
    item: str =None
    amount: int = None


class UpdateItem(SQLModel):
    item: str =None
    amount: int = None    

class CreateItem(SQLModel):
    item: str =None
    amount: int = None 

# conn_str = os.getenv("DATABASE_URL")
# engine = create_engine(conn_str)


# def create_db():
#     SQLModel.metadata.create_all(engine)


# if __name__ == "__main__":
#     create_db()
