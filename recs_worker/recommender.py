import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import json
from .db import SessionLocal, redis_client
from orders_service.infra.database.models import OrderItemORM

class RecommendationEngine:
    def __init__(self):
        self.db = SessionLocal()
        self.redis = redis_client

    def _get_order_data(self):
        query = self.db.query(OrderItemORM.order_id, OrderItemORM.product_id)
        return pd.read_sql(query.statement, self.db.bind)

    def _calculate_similarity_matrix(self, df):
        df['bought'] = 1
        matrix = df.pivot_table(index='order_id', columns='product_id', values='bought', fill_value=0)
        item_similarity = cosine_similarity(matrix.T)
        return pd.DataFrame(item_similarity, index=matrix.columns, columns=matrix.columns)

    def _persist_recommendations(self, similarity_df):
        for product_id in similarity_df.index:
            similar_items = similarity_df[product_id].sort_values(ascending=False)[1:4]
            recs = similar_items.index.tolist()
            if recs:
                self.redis.set(f"recs:product:{product_id}", json.dumps(recs))

    def run_update(self):
        try:
            df = self._get_order_data()
            if df.empty:
                return
            similarity_df = self._calculate_similarity_matrix(df)
            self._persist_recommendations(similarity_df)
        finally:
            self.db.close()
