Serializers
===========

Blog Serializers
----------------

BlogSerializer
^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize blog post data.

*Fields:*

- ``id`` (integer): The unique identifier for the blog post.
- ``title`` (string): The title of the blog post.
- ``body`` (string): The content of the blog post.
- ``thumbnail`` (string): The URL of the thumbnail image for the blog post.
- ``views`` (integer): The number of views for the blog post.
- ``author`` (nested object): The author of the blog post (serialized using CustomerSerializer).
- ``updated_at`` (datetime): The timestamp of when the blog post was last updated.
- ``comments_count`` (integer): The number of comments on the blog post.

BlogCommentSerializer
^^^^^^^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize comments on blog posts.

*Fields:*

- ``id`` (integer): The unique identifier for the comment.
- ``customer`` (nested object): The customer who posted the comment (serialized using CustomerSerializer).
- ``subject`` (string): The subject of the comment.
- ``message`` (string): The content of the comment.
- ``created_at`` (datetime): The timestamp of when the comment was created.

Shop Serializers
----------------

ProductImageSerializer
^^^^^^^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize product images.

*Fields:*

- ``id`` (integer): The unique identifier for the product image.
- ``image`` (string): The URL of the product image.

FeatureValueFullSerializer
^^^^^^^^^^^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize feature values with translations.

*Fields:*

- ``id`` (integer): The unique identifier for the feature value.
- ``translations`` (nested object): Translations for the feature value.
- ``product_count`` (integer): The number of products associated with the feature value.
- ``value`` (string): The value of the feature.

FeatureKeyFullSerializer
^^^^^^^^^^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize feature keys with translations and associated values.

*Fields:*

- ``id`` (integer): The unique identifier for the feature key.
- ``translations`` (nested object): Translations for the feature key.
- ``key_product_count`` (integer): The number of products associated with the feature key.
- ``values`` (nested object): Associated feature values (serialized using FeatureValueFullSerializer).
- ``key`` (string): The key of the feature.

FeatureKeySerializer
^^^^^^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize feature keys with translations.

*Fields:*

- ``id`` (integer): The unique identifier for the feature key.
- ``translations`` (nested object): Translations for the feature key.
- ``key`` (string): The key of the feature.

FeatureValueSerializer
^^^^^^^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize feature values with translations.

*Fields:*

- ``id`` (integer): The unique identifier for the feature value.
- ``key`` (nested object): The associated feature key (serialized using FeatureKeySerializer).
- ``translations`` (nested object): Translations for the feature value.
- ``value`` (string): The value of the feature.

MainFeatureSerializer
^^^^^^^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize main features with associated feature keys and values.

*Fields:*

- ``id`` (integer): The unique identifier for the main feature.
- ``key`` (nested object): The associated feature key (serialized using FeatureKeySerializer).
- ``value`` (nested object): The associated feature value (serialized using FeatureValueSerializer).

*Methods:*

- ``get_product_count(self, obj)``: Returns the number of products associated with the main feature.

ProductSerializer
^^^^^^^^^^^^^^^^^

The ``ProductSerializer`` is used to serialize and deserialize product data.

*Fields:*

- ``id`` (integer): The unique identifier for the product.
- ``translations`` (nested object): Translated fields for the product.
- ``inventory`` (integer): The available inventory of the product.
- ``org_price`` (decimal): The original price of the product.
- ``price`` (decimal): The discounted price of the product.
- ``price_with_tax`` (decimal): The price of the product with tax included.
- ``collection_id`` (integer): The ID of the collection to which the product belongs.
- ``promotions`` (nested object): Promotions applied to the product.
- ``value_feature`` (nested object): Additional features of the product.
- ``images`` (nested object): Images associated with the product.
- ``secondhand`` (boolean): Indicates whether the product is secondhand.
- ``title`` (string): The title of the product.
- ``description`` (string): The description of the product.
- ``slug`` (string): The slugified version of the product title.

SimpleProductSerializer
^^^^^^^^^^^^^^^^^^^^^^

The ``SimpleProductSerializer`` is used to serialize and deserialize basic product data.

*Fields:*

- ``id`` (integer): The unique identifier for the product.
- ``translations`` (nested object): Translated fields for the product.
- ``org_price`` (decimal): The original price of the product.
- ``price`` (decimal): The discounted price of the product.
- ``title`` (string): The title of the product.
- ``description`` (string): The description of the product.

CollectionSerializer
^^^^^^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize product collections with nested subcollections.

*Fields:*

- ``id`` (integer): The unique identifier for the collection.
- ``translations`` (nested object): Translations for the collection.
- ``parent`` (integer): The ID of the parent collection.
- ``products_count`` (integer): The number of products in the collection.
- ``children`` (nested object): Subcollections of the collection (serialized using CollectionSerializer).

CartItemSerializer
^^^^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize cart items with associated product details.

*Fields:*

- ``id`` (integer): The unique identifier for the cart item.
- ``product`` (nested object): The associated product (serialized using SimpleProductSerializer).
- ``quantity`` (integer): The quantity of the product in the cart.
- ``total_price`` (decimal): The total price of the cart item.

CartSerializer
^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize shopping carts with associated cart items.

*Fields:*

- ``id`` (UUID): The unique identifier for the cart.
- ``items`` (nested object): Cart items in the cart (serialized using CartItemSerializer).
- ``total_price`` (decimal): The total price of all items in the cart.
- ``org_price`` (decimal): The original total price of all items in the cart.

*Methods:*

- ``get_total_price(self, cart)``: Returns the total price of the cart.
- ``get_org_price(self, cart)``: Returns the original total price of the cart.

ApplyDiscountSerializer
^^^^^^^^^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize discount code application requests.

*Fields:*

- ``discount_code`` (string): The discount code to be applied.

AddItemsSerializer
^^^^^^^^^^^^^^^^^^

The ``AddItemsSerializer`` is used to serialize and deserialize data for adding items to a cart.

*Fields:*

- ``id`` (integer): The unique identifier for the cart item.
- ``product_id`` (integer): The ID of the product to add to the cart.
- ``quantity`` (integer): The quantity of the product to add.

*Validation:*

- ``product_id``: Must be a valid product ID.
- ``quantity``: Must be at least 1.

*Methods:*

- ``save()``: Adds the specified quantity of the product to the cart. Raises a validation error if the product ID is invalid or the quantity is less than 1.
- ``validate_product_id()``: Validates that the product ID exists in the database.
- ``validate_quantity()``: Validates that the quantity is at least 1.

UpdateItemsSerializer
^^^^^^^^^^^^^^^^^^^^

The ``UpdateItemsSerializer`` is used to serialize and deserialize data for updating items in a cart.

*Fields:*

- ``quantity`` (integer): The new quantity for the cart item.

*Methods:*

- ``save()``: Updates the quantity of the cart item. Raises a validation error if the new quantity is less than 1.

*Validation:*

- ``quantity``: Must be at least 1.

ReviewSerializer
^^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize product reviews with associated customer details.

*Fields:*

- ``id`` (integer): The unique identifier for the review.
- ``created_at`` (datetime): The date and time when the review was created.
- ``parent_review`` (integer): The ID of the parent review, if any.
- ``title`` (string): The title of the review.
- ``description`` (string): The description of the review.
- ``rating`` (integer): The rating given in the review.
- ``customer`` (nested object): Details of the customer who wrote the review (serialized using CustomerSerializer).
- ``replies`` (nested object): Replies to the review (serialized using ReviewSerializer).

OrderItemSerializer
^^^^^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize order items with associated product details.

*Fields:*

- ``product`` (nested object): The associated product (serialized using SimpleProductSerializer).
- ``price`` (decimal): The price of the product.
- ``quantity`` (integer): The quantity of the product in the order.

OrderSerializer
^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize orders with associated order items and customer details.

*Fields:*

- ``id`` (integer): The unique identifier for the order.
- ``order_status`` (string): The status of the order.
- ``customer`` (nested object): Details of the customer who placed the order (serialized using CustomerSerializer).
- ``phone_number`` (string): The phone number of the customer.
- ``email`` (string): The email address of the customer.
- ``zip_code`` (string): The zip code of the customer's address.
- ``path`` (string): The path of the customer's address.
- ``city`` (string): The city of the customer's address.
- ``province`` (string): The province of the customer's address.
- ``first_name`` (string): The first name of the customer.
- ``last_name`` (string): The last name of the customer.
- ``orders`` (nested object): Order items in the order (serialized using OrderItemSerializer).
- ``total_price`` (decimal): The total price of the order.


CreateOrderSerializer
^^^^^^^^^^^^^^^^^^^^^

The ``CreateOrderSerializer`` is used to serialize and deserialize data for creating an order from a cart.

*Fields:*

- ``cart_id`` (UUID): The ID of the cart from which the order will be created.

*Validation:*

- ``cart_id``: Must be a valid UUID corresponding to an existing cart in the database.

*Methods:*

- ``save()``: Creates an order from the specified cart. Raises a validation error if the cart ID is invalid or the cart is empty.


CustomerSerializer
^^^^^^^^^^^^^^^^^^^

The ``CustomerSerializer`` is used to serialize customer data.

*Fields:*

- ``id`` (integer): The unique identifier for the customer.
- ``first_name`` (string): The first name of the customer.
- ``last_name`` (string): The last name of the customer.
- ``user_id`` (integer): The ID of the associated user.
- ``birth_date`` (date): The birth date of the customer.
- ``membership`` (string): The membership status of the customer.

*Read-only Fields:*

- ``id``
- ``user_id``
- ``membership``

``CustomerSerializer`` is read-only, used for serializing customer data retrieved from the database.

ReportingSerializer
^^^^^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize reporting parameters for generating reports.

*Fields:*

- ``days`` (integer): The number of days for the report.
- ``start_at`` (datetime): The start date for the report.
- ``end_at`` (datetime): The end date for the report.

VerifySerializer
^^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize requests to verify transactions.

*Fields:*

- ``order`` (integer): The ID of the order associated with the transaction.
- ``total_price`` (decimal): The total price of the transaction.
- ``Authority`` (string): The authority code for the transaction.

SendRequestSerializer
^^^^^^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize requests to send transaction requests.

*Fields:*

- ``phone_number`` (string): The phone number associated with the transaction request.
- ``total_price`` (decimal): The total price of the transaction request.

UpdateTransactionSerializer
^^^^^^^^^^^^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize requests to update transaction details.

*Fields:*

- ``payment_status`` (string): The updated payment status of the transaction.
- ``receipt_number`` (string): The receipt number of the transaction.

AuditLogSerializer
^^^^^^^^^^^^^^^^^^

This serializer is used to serialize audit log entries.

*Fields:*

- ``user`` (nested object): Details of the user associated with the action.
- ``action`` (string): The action performed.
- ``timestamp`` (datetime): The timestamp of the action.
- ``table_name`` (string): The name of the table affected.
- ``row_id`` (integer): The ID of the row affected.
- ``changes`` (string): Details of the changes made.

PromotionSerializer
^^^^^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize promotions.

*Fields:*

- ``id`` (integer): The unique identifier for the promotion.
- ``translations`` (nested object): Translations for the promotion title and description.
- ``title`` (string): The title of the promotion.
- ``description`` (string): The description of the promotion.


SiteSettingsSerializer
^^^^^^^^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize site settings.

*Fields:*

- ``id`` (integer): The unique identifier for the site settings.
- ``phone_number`` (string): The phone number displayed on the site.
- ``logo`` (string): The URL of the site's logo.
- ``telegram_link`` (string): The link to the Telegram channel.
- ``twitter_link`` (string): The link to the Twitter page.
- ``instagram_link`` (string): The link to the Instagram profile.
- ``whatsapp_link`` (string): The link to the WhatsApp contact.
- ``translations`` (nested object): Translations for the footer text and address.
- ``footer_text`` (string): The text displayed in the site footer.
- ``address`` (string): The address of the business.

HomeBannerSerializer
^^^^^^^^^^^^^^^^^^^^

This serializer is used to serialize and deserialize home banners.

*Fields:*

- ``id`` (integer): The unique identifier for the home banner.
- ``product`` (nested object): The products featured in the home banner.