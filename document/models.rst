Models
------

Blog App
~~~~~~~~

Blog
^^^^
The ``Blog`` model represents a blog post in the system.

- **Fields**:

  - ``title``: Title of the blog post.
  - ``body``: Body content of the blog post.
  - ``thumbnail``: Image thumbnail for the blog post.
  - ``views``: Number of views the blog post has.
  - ``author``: Author of the blog post.

BlogComment
^^^^^^^^^^^
The ``BlogComment`` model represents a comment on a blog post.

- **Fields**:

  - ``customer``: The customer who posted the comment.
  - ``blog``: The blog post the comment is associated with.
  - ``subject``: Subject of the comment.
  - ``message``: Content of the comment.
  - ``active``: Boolean field indicating whether the comment is active or not.

Discount App
~~~~~~~~~~~~

BaseDiscount
^^^^^^^^^^^^
The ``BaseDiscount`` model represents a base discount available in the system.

- **Fields**:

  - ``discount``: The discount value.
  
  - ``active``: Boolean field indicating whether the discount is active or not.

  - ``code``: Discount code (optional).

  - ``valid_from``: Start date of the discount validity period.

  - ``valid_to``: End date of the discount validity period.

  - ``mode``: The mode of the discount.
  - ``limit_price``: The minimum price required for the discount to apply.
  - ``max_price``: The maximum price for which the discount is applicable.

Core App
~~~~~~~~

BaseModel
^^^^^^^^^
The ``BaseModel`` class serves as the base model for other models in the system, providing common fields and functionality such as created_at, updated_at, and logical deletion.

- **Fields**:

  - ``created_at``: The datetime when the object was created.
  - ``updated_at``: The datetime when the object was last updated.
  - ``deleted_at``: The datetime when the object was soft-deleted.

AuditLog
^^^^^^^^
The ``AuditLog`` model records changes made to other models in the system.

- **Fields**:

  - ``user``: The user who performed the action.
  - ``action``: The type of action performed (CREATE, UPDATE, DELETE).
  - ``timestamp``: The datetime when the action was performed.
  - ``table_name``: The name of the table/model being modified.
  - ``row_id``: The ID of the modified row.
  - ``old_value``: The previous value of the modified row.
  - ``changes``: The changes made to the row.

User
^^^^
The ``User`` model represents a user in the system.

- **Fields**:

  - ``phone_number``: The user's phone number.
  - ``email``: The user's email address.
  - ``password``: The user's password (hashed).
  - ``is_active``: Boolean field indicating whether the user is active.
  - ``is_staff``: Boolean field indicating whether the user is a staff member.
  - ``last_login``: The datetime when the user last logged in.

Shop App
~~~~~~~~

Customer
^^^^^^^^
The ``Customer`` model represents a customer in the system.

- **Fields**:

  - ``first_name``: The customer's first name.
  - ``last_name``: The customer's last name.
  - ``birth_date``: The customer's birth date.
  - ``membership``: The customer's membership status.
  - ``user``: The user associated with the customer.

Cart
^^^^
The ``Cart`` model represents a shopping cart in the system.

- **Fields**:

  - ``customer``: The customer who owns the cart.
  - ``discount``: The discount applied to the cart.

CartItem
^^^^^^^^
The ``CartItem`` model represents an item in a shopping cart.

- **Fields**:

  - ``cart``: The cart to which the item belongs.
  - ``product``: The product being added to the cart.
  - ``quantity``: The quantity of the product in the cart.

Address
^^^^^^^
The ``Address`` model represents a customer's address in the system.

- **Fields**:

  - ``zip_code``: The postal code of the address.
  - ``path``: The street address.
  - ``city``: The city of the address.
  - ``province``: The province of the address.
  - ``customer``: The customer associated with the address.
  - ``default``: Boolean field indicating whether the address is the default address for the customer.

Order
^^^^^
The ``Order`` model represents an order placed by a customer.

- **Fields**:

  - ``order_status``: The status of the order.
  - ``customer``: The customer who placed the order.
  - ``zip_code``: The postal code of the order.
  - ``path``: The street address of the order.
  - ``city``: The city of the order.
  - ``province``: The province of the order.
  - ``first_name``: The first name of the customer placing the order.
  - ``last_name``: The last name of the customer placing the order.
  - ``discount``: The discount applied to the order.

OrderItem
^^^^^^^^^
The ``OrderItem`` model represents an item in an order.

- **Fields**:

  - ``order``: The order to which the item belongs.
  - ``product``: The product being ordered.
  - ``unit_price``: The unit price of the product.
  - ``quantity``: The quantity of the product ordered.

Review
^^^^^^
The ``Review`` model represents a review left by a customer for a product.

- **Fields**:

  - ``customer``: The customer who left the review.
  - ``product``: The product being reviewed.
  - ``rating``: The rating given by the customer.
  - ``title``: The title of the review.
  - ``description``: The description of the review.
  - ``parent_review``: The parent review if this is a reply to another review.
  - ``active``: Boolean field indicating whether the review is active.

Transaction
^^^^^^^^^^^
The ``Transaction`` model represents a transaction associated with an order.

- **Fields**:

  - ``order``: The order associated with the transaction.
  - ``payment_status``: The payment status of the transaction.
  - ``total_price``: The total price of the transaction.
  - ``customer``: The customer associated with the transaction.
  - ``receipt_number``: The receipt number of the transaction.
  - ``phone_number``: The phone number associated with the transaction.
  - ``Authority``: The authority of the transaction.

Promotion
^^^^^^^^^
The `Promotion` model represents a promotion in the system.

- **Fields**:

  - ``title``: The title of the promotion.
  - ``description``: The description of the promotion.

Collection
^^^^^^^^^^
The ``Collection`` model represents a collection of products in the system.

- **Fields**:

  - ``title``: The title of the collection.
  - ``parent``: The parent collection if this is a subcollection.

Product
^^^^^^^
The ``Product`` model represents a product in the system.

- **Fields**:

  - ``title``: The title of the product.
  - ``description``: The description of the product.
  - ``unit_price``: The unit price of the product.
  - ``inventory``: The inventory count of the product.
  - ``collection``: The collection to which the product belongs.
  - ``promotions``: The promotions associated with the product.
  - ``discount``: The discount applied to the product.
  - ``secondhand``: Boolean field indicating whether the product is secondhand.

ProductImage
^^^^^^^^^^^^
The `ProductImage` model represents an image associated with a product.

- **Fields**:

  - ``product``: The product associated with the image.
  - ``image``: The image file.

Feature Key
^^^^^^^^^^^^

Model representing a feature key.

Attributes:
    - ``key`` (CharField): The key of the feature.

Meta:
    - ``verbose_name``: "Feature Key"
    - ``verbose_name_plural``: "Feature Keys"

Methods:
    - ``__repr__``: Return a string representation of the feature key.
    - ``__str__``: Return a string representation of the feature key.


Feature Value
^^^^^^^^^^^^

Model representing a feature value.

Attributes:
    - ``key`` (ForeignKey): The feature key.
    - ``value`` (CharField): The value of the feature.

Meta:
    - ``verbose_name``: "Feature Value"
    - ``verbose_name_plural``: "Feature Values"

Methods:
    - ``__repr__``: Return a string representation of the feature value.
    - ``__str__``: Return a string representation of the feature value.


Main Feature
^^^^^^^^^^^^

Model representing a main feature.

Attributes:
    - ``product`` (ForeignKey): The product associated with the main feature.
    - ``key`` (ForeignKey): The feature key.
    - ``value`` (ForeignKey): The feature value.

Meta:
    - ``verbose_name``: "Main Feature"
    - ``verbose_name_plural``: "Main Features"

Methods:
    - ``__repr__``: Return a string representation of the main feature.
    - ``__str__``: Return a string representation of the main feature.