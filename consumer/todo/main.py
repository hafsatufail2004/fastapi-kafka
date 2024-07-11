from code.todo.model import CreateItem, UpdateItem
from code.todo.services.consumer_services import delete_item_id, update_item_id
from fastapi import FastAPI,Depends
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from contextlib import asynccontextmanager
from sqlmodel import Field, SQLModel
from typing import Optional, AsyncGenerator, Annotated
import todo_pb2
import asyncio
from code.todo.services.comsumer_services import get_data,get_item_by_id,add_item
from database import *

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str


async def consume(topic: str, bootstrap_servers: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="my-group",
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.value)
            # Decrialized Data
            get_data = todo_pb2.Todo_Proto()
            get_data.ParseFromString(msg.value)
            print(f"Decrialized Data : ", get_data)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

# 
# @asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncGenerator:
    # print("Consumer Start ....")
    # asyncio.create_task(consume(topic="todos", bootstrap_servers="broker:19092"))
    # yield
# 

# 
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
     print("Creating tables ....")
     create_tables()
     yield
     print("Shutting down...")


app: FastAPI = FastAPI(lifespan=lifespan)


@app.get("/")
def get():
    return {"message": "Hello World"}


@app.get("/item")
def get_item(session:Annotated[Session , Depends(get_session)]):
    return get_data(session=session)

@app.get("/item/{item_id}")
def get_data_by_id(item_id:int,session:Annotated[Session,Depends(get_session)]):
    return get_item_by_id(item_id=item_id,session=session)


@app.post("/add_item")
def create_item(item:CreateItem,session:Annotated[Session , Depends(get_session)]):
    return add_item(item=item,session=session)
    
@app.put("/update_item/{item_id}")
def update_item(item_id:int,item_update:UpdateItem,session:Annotated[Session , Depends(get_session)]):
    return update_item_id(item_id=item_id,item_update=item_update,session=session)

@app.delete("delete_item/{item_id}")
def delete_item(item_id:int,session:Annotated[Session , Depends(get_session)]):
    return delete_item_id(item_id=item_id,session=session)
    





























@app.post("/add_data")
async def add_data_kafka(todo: Todo):
    producer = AIOKafkaProducer(bootstrap_servers="broker:19092")
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        add_data = todo_pb2.Todo_Proto(
            name=todo.name,
            description=todo.description,
        )
        # Serialize Data
        protoc_data = add_data.SerializeToString()
        print(f"Serialized Data : ", protoc_data)
        # Produce message
        await producer.send_and_wait(topic="todos", value=protoc_data)
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()
    return todo.model_dump_json()
