from django.conf import settings


class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        self.request= request
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price_after_off)}
        if override_quantity:
            self.cart[product_id]['quantity'] = int(quantity)
        else:
            self.cart[product_id]['quantity'] += int(quantity)
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        # self.cart =  json.loads(self.cart)
        # del self.request.session
        # self.cart =  eval(self.cart)
        print(self.cart)
        print(type(self.cart))
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Food.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            # item['price'] = Decimal(item['price'])
            # item['quantity'] = Decimal(item['quantity'])
            item['total_price'] = Decimal(item['price']) * Decimal(item['quantity'])
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.
                   cart.values())

    def clear(self):
        # remove cart from session

        print('start clear')
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def edit_orders(self, order_id):
        self.cart.clear()
        print('done clear')
        products = OrderItem.objects.filter(order_id=order_id)
        print('done get product')
        for product in products:
            self.add(product=product.product,
                     quantity=product.quantity,
                     override_quantity=True)
        print('done add product')
        order = Order.objects.get(pk=order_id)
        print('done get order product')
        order.status = "C"
        order.save()
        self.save()
        print('done save order product')

    @property
    def offkey(self):
        if self.offkey_id and self.offkey_id != 'None':
            try:
                return Offkey.objects.get(id=self.offkey_id)
            except Offkey.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.offkey:
            return (self.offkey.discount / Decimal(100)) \
                * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
