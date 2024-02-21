import random

from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    """
    run locust web server
        locust -f Locust_PerformanceTest/browse_products.py
    """
    wait_time = between(1, 5)

    @task(2)
    def view_products(self):
        collection_id = 1
        self.client.get(f'/api-v1/products/?collection_id={collection_id}',
                        name='/api-v1/products')

    @task(4)
    def view_product(self):
        product_id = random.randint(1, 3)
        self.client.get(f'/api-v1/products/{product_id}',
                        name='/api-v1/products/:id')

    @task(1)
    def add_to_cart(self):
        product_id = random.randint(1, 3)
        self.client.post(f'/api-v1/cart/{self.cart_id}/items',
                         name='/api-v1/cart/items',
                         json={'product_id': product_id, 'quantity': 1})

    def on_start(self):
        response = self.client.post('/api-v1/cart/')
        result = response.json()
        self.cart_id = result['id']
