import time
import logging
from .app import app

logger = logging.getLogger(__name__)

@app.task(name="ml_worker.tasks.test_task")
def test_task(x, y):
    logger.info(f"Executing test task for {x} and {y}")
    time.sleep(5)  
    result = x + y
    logger.info(f"Test task finished with result: {result}")
    return result

@app.task(name="ml_worker.tasks.calculate_recommendations")
def calculate_recommendations():
    logger.info("Starting recommendation calculation...")
    time.sleep(2)
    logger.info("Recommendation calculation finished!")
    return True
