import logging
import random
from .app import app
from .db import SessionLocal
from .recommender import RecommendationEngine
from orders_service.infra.database.models import OrderORM, OrderItemORM
from orders_service.app.schemas.orders_schemas import OrderStatus

logger = logging.getLogger(__name__)

@app.task(name="recs_worker.tasks.generate_dummy_data")
def generate_dummy_data(count=100):
    db = SessionLocal()
    try:
        usernames = ["alexey", "ivan", "maria", "john", "doe"]
        product_ids = [101, 102, 103, 104, 105, 201, 202, 203]
        
        for _ in range(count):
            order = OrderORM(
                username=random.choice(usernames),
                status=OrderStatus.CREATED
            )
            db.add(order)
            db.flush()
            
            num_items = random.randint(1, 3)
            selected_products = random.sample(product_ids, num_items)
            
            for p_id in selected_products:
                item = OrderItemORM(
                    order_id=order.id,
                    product_id=p_id,
                    quantity=random.randint(1, 2),
                    price=random.uniform(500, 2000)
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
