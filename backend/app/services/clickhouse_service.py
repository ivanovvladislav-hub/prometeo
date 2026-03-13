# from datetime import datetime, timedelta
# from app.models.database import clickhouse_client
# from app.models.schemas import MetricCreate

# class ClickHouseService:

#     @staticmethod
#     def insert_metric(metric: MetricCreate):
#         """Вставка одной метрики"""
#         timestamp = metric.timestamp or datetime.now()
#         query = """
#         INSERT INTO metrics (timestamp, sensor_id, value)
#         VALUES
#         """
#         clickhouse_client.execute(
#             query,
#             [(timestamp, metric.sensor_id, metric.value)]
#         )

#     @staticmethod
#     def insert_metrics_batch(metrics: list[MetricCreate]):
#         """Массовая вставка метрик (быстрее)"""
#         data = []
#         for metric in metrics:
#             timestamp = metric.timestamp or datetime.now()
#             data.append((timestamp, metric.sensor_id, metric.value))

#         query = "INSERT INTO metrics (timestamp, sensor_id, value) VALUES"
#         clickhouse_client.execute(query, data)

#     @staticmethod
#     def get_statistics(sensor_id: int, hours: int = 24):
#         """Получение статистики за последние N часов"""
#         time_from = datetime.now() - timedelta(hours=hours)

#         query = """
#         SELECT
#             sensor_id,
#             avg(value) as avg_value,
#             min(value) as min_value,
#             max(value) as max_value,
#             count(*) as count,
#             min(timestamp) as period_start,
#             max(timestamp) as period_end
#         FROM metrics
#         WHERE sensor_id = %(sensor_id)s
#           AND timestamp >= %(time_from)s
#         GROUP BY sensor_id
#         """

#         result = clickhouse_client.execute(
#             query,
#             {'sensor_id': sensor_id, 'time_from': time_from}
#         )

#         return result[0] if result else None

#     @staticmethod
#     def get_timeseries(sensor_id: int, hours: int = 24, interval_minutes: int = 5):
#         """Получение временного ряда для графика"""
#         time_from = datetime.now() - timedelta(hours=hours)

#         query = f"""
#         SELECT
#             toStartOfInterval(timestamp, INTERVAL {interval_minutes} MINUTE) as time_bucket,
#             avg(value) as avg_value
#         FROM metrics
#         WHERE sensor_id = %(sensor_id)s
#           AND timestamp >= %(time_from)s
#         GROUP BY time_bucket
#         ORDER BY time_bucket
#         """

#         result = clickhouse_client.execute(
#             query,
#             {'sensor_id': sensor_id, 'time_from': time_from}
#         )

#         return [{"timestamp": row[0], "value": row[1]} for row in result]
