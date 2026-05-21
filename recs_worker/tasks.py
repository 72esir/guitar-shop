import logging
import random
from .app import app
from .db import SessionLocal
from .recommender import RecommendationEngine
from orders_service.infra.database.models import OrderORM, OrderItemORM, GuitarType, PickupConfig
from orders_service.app.schemas.orders_schemas import OrderStatus

logger = logging.getLogger(__name__)

@app.task(name="recs_worker.tasks.generate_dummy_data")
def generate_dummy_data(count=100):
    db = SessionLocal()
    try:
        usernames = ["alexey", "ivan", "maria", "john", "doe"]
        products = [
            {"id": 101, "title": "Fender Stratocaster", "sku": "FND-STR-01", "brand": "Fender", "type": GuitarType.ELECTRIC, "pickup": PickupConfig.SSS},
            {"id": 102, "title": "Gibson Les Paul", "sku": "GBS-LP-02", "brand": "Gibson", "type": GuitarType.ELECTRIC, "pickup": PickupConfig.HH},
            {"id": 103, "title": "Ibanez RG", "sku": "IBZ-RG-03", "brand": "Ibanez", "type": GuitarType.ELECTRIC, "pickup": PickupConfig.HH},
            {"id": 104, "title": "PRS Custom 24", "sku": "PRS-C24-04", "brand": "PRS", "type": GuitarType.ELECTRIC, "pickup": PickupConfig.HH},
            {"id": 105, "title": "Yamaha Pacifica", "sku": "YMH-PAC-05", "brand": "Yamaha", "type": GuitarType.ELECTRIC, "pickup": PickupConfig.HSS},
            {"id": 201, "title": "Martin D-28", "sku": "MRT-D28-06", "brand": "Martin", "type": GuitarType.ACOUSTIC, "pickup": PickupConfig.NONE},
            {"id": 202, "title": "Taylor 214ce", "sku": "TYL-214-07", "brand": "Taylor", "type": GuitarType.ACOUSTIC, "pickup": PickupConfig.PIEZO},
            {"id": 203, "title": "Epiphone EJ-200", "sku": "EPI-EJ200-08", "brand": "Epiphone", "type": GuitarType.ACOUSTIC, "pickup": PickupConfig.NONE},
        ]
        
        for _ in range(count):
            order = OrderORM(
                username=random.choice(usernames),
                status=OrderStatus.CREATED
            )
            db.add(order)
            db.flush()
            
            num_items = random.randint(1, 3)
            selected_products = random.sample(products, num_items)
            
            for p in selected_products:
                item = OrderItemORM(
                    order_id=order.id,
                    product_id=p["id"],
                    title=p["title"],
                    sku=p["sku"],
                    brand=p["brand"],
                    quantity=random.randint(1, 2),
                    price=random.uniform(500, 2000),
                    type=p["type"],
                    body_wood="Alder",
                    neck_wood="Maple",
                    fretboard_wood="Rosewood",
                    fret_count=22,
                    scale_length=25.5,
                    pickup_config=p["pickup"]
                )
                db.add(item)
        
        db.commit()
        logger.info(f"Generated {count} dummy orders")
    except Exception as e:
        db.rollback()
        logger.error(f"Error generating data: {e}")
    finally:
        db.close()

@app.task(name="recs_worker.tasks.calculate_recommendations")
def calculate_recommendations():
    logger.info("Recommendation calculation started")
    try:
        engine = RecommendationEngine()
        engine.run_update()
        logger.info("Recommendation calculation finished successfully")
        return True
    except Exception as e:
        logger.error(f"Error in recommendation calculation: {e}")
        return False
