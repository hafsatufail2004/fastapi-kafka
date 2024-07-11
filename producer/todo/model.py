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





