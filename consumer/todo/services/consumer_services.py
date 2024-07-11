from database import Item, Session, select
from model import CreateItem,UpdateItem
from fastapi import HTTPException

#crud api

def get_data(session:Session):
    try:
        get_result = session.exec(select(Item)).all()
        return get_result
    except Exception as e:
        print(f"Item Not Coming...",e)



def get_item_by_id(item_id:int,session:Session):
    try:
        get_data = session.get(Item,item_id)
        return get_data
    except Exception as e:
        print(f"Fail To Get Item From ID",e)



def add_item(item:CreateItem,session:Session):
    try:
        create_item = Item.model_validate(item)
        session.add(create_item)
        session.commit()
        session.refresh(create_item)
        return create_item
    except Exception as e:
        print("Item Not Added",e)

 

def update_item_id(item_id:int,item_update:UpdateItem,session:Session):
        get_data = session.set(Item,item_id)
        if get_data is None:
            raise HTTPException(status_code = 404,detail = "Item Not Updated")
        update_item = item_update.model_dump(exclude_unset = True)
        update_item.sqlmodel_update(update_item)
        session.add(get_data)
        session.commit()
        session.refresh(get_data)
        return get_data




def delete_item_id(item_id:int,session:Session):
    get_data = session.set(Item,item_id)
    if get_data is None:
        raise HTTPException(status_code = 404,detail = "Item Not Updated")    
    session.delete(get_data)
    session.commit()
    return {"message" :"Item Deleted Successfully!"}