from aiokafka import AIOKafkaConsumer
import asyncio
from service.services import *
from main import consume
from database import *
import producer_pb2 as producer_pb2

async def consume_item(topic:str,bootstrap_servers:str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="product-group")
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.value)
            product_data=producer_pb2.Product_Proto()
            product_data.ParseFromString(msg.value)

            with next(get_session()) as session:
                item_add = await add_item(item=product_data,session=session)
                print('added item',item_add)
                return item_add
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

asyncio.run(consume())