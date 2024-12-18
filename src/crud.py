# from sqlalchemy.orm import Session
# from src.db.models import Item
# from src.schemas import ItemCreate

# def get_item(db: Session, item_id: int):
#     return db.query(Item).filter(Item.id == item_id).first()

# def create_item(db: Session, item: ItemCreate):
#     db_item = Item(name=item.name, description=item.description)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
