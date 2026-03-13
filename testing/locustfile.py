from locust import HttpUser, task, between

class PrometeoUser(HttpUser):
    # Время ожидания между задачами (от 1 до 3 секунд)
    wait_time = between(1, 3)

    @task(3)  # Вес задачи: будет выполняться чаще
    def send_metric(self):
        # Отправляем данные с датчика
        self.client.post("/api/metric", json={
            "sensor_id": 1,
            "value": 22.5
        })

    @task(1)
    def get_stats(self):
        # Запрашиваем статистику
        self.client.get("/api/stats/1")
