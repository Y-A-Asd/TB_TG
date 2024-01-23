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
        self.client.get(f'/shop/products/?collection_id={collection_id}',
                        name='/shop/products')

    @task(4)
    def view_product(self):
        product_id = random.randint(1, 3)
        self.client.get(f'/shop/products/{product_id}',
                        name='/shop/products/:id')

    @task(1)
    def add_to_cart(self):
        product_id = random.randint(1, 3)
        self.client.post(f'/shop/cart/{self.cart_id}/items',
                         name='/shop/cart/items',
                         json={'product_id': product_id, 'quantity': 1})

    def on_start(self):
        response = self.client.post('/shop/cart/')
        result = response.json()
        self.cart_id = result['id']
