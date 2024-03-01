Views
-----


Blog Views
~~~~~~~~

BlogViewSet
^^^^^^^^^^^

The ``BlogViewSet`` provides API endpoints to retrieve and manipulate blog posts.

- Retrieve and List Blogs:

  - Endpoint: ``/blogs/``
  - Methods: ``GET``
  - Description: Retrieves a list of blog posts or a single blog post by its ID.
  - Parameters:

    - None

- Retrieve Blog with View Count Update:

  - Endpoint: ``/blogs/<blog_id>/``
  - Methods: ``GET``
  - Description: Retrieves a single blog post by its ID and updates its view count.
  - Parameters:

    - ``blog_id``: The ID of the blog post.

BlogCommentViewSet
^^^^^^^^^^^

The ``BlogCommentViewSet`` provides API endpoints to retrieve and manipulate comments on blog posts.

- List and Create Blog Comments:

  - Endpoint: ``/blogs/<blog_id>/comments/``
  - Methods: ``GET``, ``POST``
  - Description: Retrieves a list of comments for a specific blog post or adds a new comment to the blog post.
  - Parameters:

    - ``blog_id``: The ID of the blog post.

- Retrieve, Update, and Delete Blog Comments:

  - Endpoint: ``/blogs/<blog_id>/comments/<comment_id>/``
  - Methods: ``GET``, ``PUT``, ``DELETE``
  - Description: Retrieves, updates, or deletes a specific comment on a blog post.
  - Parameters:

    - ``blog_id``: The ID of the blog post.
    - ``comment_id``: The ID of the comment.

Core Views
~~~~~~~~

UserCreateView
^^^^^^^^^^^

The ``UserCreateView`` provides API endpoints for user registration.

- Create User:

  - Endpoint: ``/users/create/``
  - Methods: ``POST``
  - Description: Registers a new user in the system.
  - Parameters:

    - ``phone_number``: The phone number of the user.

UserLoginOTPView
^^^^^^^^^^^

The ``UserLoginOTPView`` provides API endpoints for user login using OTP.

- Generate and Send OTP:

  - Endpoint: ``/users/login/otp/``
  - Methods: ``POST``
  - Description: Generates and sends an OTP to the user's email for login.
  - Parameters:

    - ``email``: The email of the user.

VerifyOtpView
^^^^^^^^^^^

The ``VerifyOtpView`` provides API endpoints for verifying the OTP during login.

- Verify OTP:

  - Endpoint: ``/users/login/otp/verify/``
  - Methods: ``POST``
  - Description: Verifies the OTP provided by the user during login.
  - Parameters:
  
    - ``email``: The email of the user.
    - ``otp``: The OTP provided by the user.

Shop Views
~~~~~~~~

ProductViewSet
^^^^^^^^^^^

The ``ProductViewSet`` provides API endpoints to retrieve and manipulate products.

- List Products:

  - Endpoint: ``/products/``
  - Methods: ``GET``
  - Description: Retrieves a list of products with optional filtering and search capabilities.
  - Parameters:

    - Various query parameters for filtering and searching.

- Retrieve, Create, Update, and Delete Products:

  - Endpoint: ``/products/<product_id>/``
  - Methods: ``GET``, ``POST``, ``PUT``, ``DELETE``
  - Description: Retrieves, creates, updates, or deletes a specific product by its ID.
  - Parameters:

    - ``product_id``: The ID of the product.

CollectionViewSet
^^^^^^^^^^^

The ``CollectionViewSet`` provides API endpoints to retrieve collections and associated products.

- List Collections:

  - Endpoint: ``/collections/``
  - Methods: ``GET``
  - Description: Retrieves a list of collections with associated product counts.
  - Parameters:

    - None

- Retrieve Collection with Associated Products:

  - Endpoint: ``/collections/<collection_id>/``
  - Methods: ``GET``
  - Description: Retrieves a specific collection by its ID with associated products.
  - Parameters:
  
    - ``collection_id``: The ID of the collection.

ReviewViewSet
^^^^^^^^^^^

The ``ReviewViewSet`` provides API endpoints to retrieve and manipulate product reviews.

- List, Create, and Retrieve Reviews:

  - Endpoint: ``/products/<product_id>/reviews/``
  - Methods: ``GET``, ``POST``
  - Description: Retrieves a list of reviews for a specific product, adds a new review, or retrieves a specific review.
  - Parameters:

    - ``product_id``: The ID of the product.

- List Review Replies:

  - Endpoint: ``/products/<product_id>/reviews/<review_id>/replies/``
  - Methods: ``GET``
  - Description: Retrieves a list of replies to a specific review.
  - Parameters:

    - ``product_id``: The ID of the product.
    - ``review_id``: The ID of the review.

PromotionViewSet
^^^^^^^^^^^

The ``PromotionViewSet`` provides API endpoints to retrieve promotions and associated products.

- List Promotions:

  - Endpoint: ``/promotions/``
  - Methods: ``GET``
  - Description: Retrieves a list of promotions with associated products.
  - Parameters:

    - None


CartViewSet
^^^^^^^^^^^

The ``CartViewSet`` provides API endpoints to manipulate shopping carts.

- Create, Retrieve, and Delete Cart:

  - Endpoint: ``/cart/``
  - Methods: ``POST``, ``GET``, ``DELETE``
  - Description: Creates a new cart, retrieves an existing cart, or deletes a cart.
  - Parameters:

    - None

- Apply Discount to Cart:

  - Endpoint: ``/cart/<cart_id>/apply_discount/``
  - Methods: ``GET``, ``POST``
  - Description: Retrieves discount information or applies a discount to the cart.
  - Parameters:

    - ``cart_id``: The ID of the cart.

CartItemViewSet
^^^^^^^^^^^

The ``CartItemViewSet`` provides API endpoints to manipulate cart items.

- List, Create, Update, and Delete Cart Items:

  - Endpoint: ``/cart/<cart_id>/items/``
  - Methods: ``GET``, ``POST``, ``PATCH``, ``DELETE``
  - Description: Retrieves, adds, updates, or deletes cart items for a specific cart.
  - Parameters:

    - ``cart_id``: The ID of the cart.

CustomerViewSet
^^^^^^^^^^^

The ``CustomerViewSet`` provides API endpoints to manipulate customer profiles.

- List and Update Customers:

  - Endpoint: ``/customers/``
  - Methods: ``GET``, ``PUT``
  - Description: Retrieves a list of customers or updates a customer's profile.
  - Parameters:

    - None

- Retrieve Customer Profile and History:

  - Endpoint: ``/customers/me/``
  - Methods: ``GET``, ``PUT``
  - Description: Retrieves or updates the profile of the currently authenticated user.
  - Parameters:

    - None

- Retrieve Customer Order History:

  - Endpoint: ``/customers/<customer_id>/history/``
  - Methods: ``GET``
  - Description: Retrieves the order history of a specific customer.
  - Parameters:

    - ``customer_id``: The ID of the customer.


OrderViewSet
^^^^^^^^^^^

The ``OrderViewSet`` provides API endpoints to manipulate orders.

- List, Create, Retrieve, Update, and Delete Orders:

  - Endpoint: ``/orders/``
  - Methods: ``GET``, ``POST``, ``PATCH``


TransactionViewSet
^^^^^^^^^^^

The ``TransactionViewSet`` provides API endpoints to manage transactions.

- List, Create, Retrieve, Update, and Delete Transactions:

  - Endpoint: ``/transactions/``
  - Methods: ``GET``, ``POST``, ``PATCH``, ``DELETE``
  - Description: Retrieves a list of transactions, creates a new transaction, retrieves, updates, or deletes a transaction.
  - Parameters:

    - None

PromotionViewSet
^^^^^^^^^^^

The ``PromotionViewSet`` provides CRUD operations for promotions.

- Promotion Endpoint:

  - Endpoint: ``/promotions/``
  - Methods: ``GET``, ``POST``, ``PUT``, ``PATCH``, ``DELETE``
  - Description: Manages promotions.
  - Parameters:

    - None


SiteSettingsViewSet
^^^^^^^^^^^

The ``SiteSettingsViewSet`` provides CRUD operations for site settings.

- Site Settings Endpoint:

  - Endpoint: ``/site-settings/``
  - Methods: ``GET``, ``POST``, ``PUT``, ``PATCH``, ``DELETE``
  - Description: Manages site settings.
  - Parameters:

    - None


HomeBannerViewSet
^^^^^^^^^^^

The ``HomeBannerViewSet`` provides CRUD operations for home banners.

- Home Banners Endpoint:

  - Endpoint: ``/home-banners/``
  - Methods: ``GET``
  - Description: Manages home banners.
  - Parameters:

    - None


FeatureViewSet
^^^^^^^^^^^

The ``FeatureViewSet`` provides CRUD operations for product features.

- Features Endpoint:

  - Endpoint: ``/features/``
  - Methods: ``GET``, ``POST``, ``PUT``, ``PATCH``, ``DELETE``
  - Description: Manages product features.
  - Parameters:

    - None

ReportingAPIView
^^^^^^^^^^^

The ``ReportingAPIView`` provides an endpoint to generate various reports.

- Reporting Endpoint:

  - Endpoint: ``/reporting/``
  - Method: ``POST``
  - Description: Generates reports based on the provided parameters.
  - Parameters:

    - ``days``: Number of days to generate the report for.


Compare Products API
^^^^^^^^^^^

The ``compare_products`` view compares multiple products based on their attributes.

- Compare Products Endpoint:

  - Endpoint: ``/compare/``
  - Method: ``GET``
  - Description: Compares products based on their attributes.
  - Parameters:

    - ``product_ids``: List of product IDs to compare.



VerifyAPIView
^^^^^^^^^^^

The ``VerifyAPIView`` verifies payments made through a payment gateway.

- Payment Verification Endpoint:

  - Endpoint: ``/payment-verify/``
  - Method: ``POST``
  - Description: Verifies payments made through a payment gateway.
  - Parameters:

    - ``order_id``: ID of the order for which payment is being verified.
    - ``total_price``: Total price of the order.
    - ``Authority``: Authorization code provided by the payment gateway.


AddressViewSet
^^^^^^^^^^^

The ``AddressViewSet`` provides CRUD operations for user addresses.

- Address Endpoint:

  - Endpoint: ``/addresses/``
  - Methods: ``GET``, ``POST``, ``PUT``, ``PATCH``, ``DELETE``
  - Description: Manages user addresses.
  - Parameters:
  
    - None