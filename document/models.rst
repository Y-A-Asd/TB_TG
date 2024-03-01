Models
------

Blog App
~~~~~~~~

Blog
^^^^
The `Blog` model represents a blog post in the system.

- **Fields**:
  - `title`: Title of the blog post.
  - `body`: Body content of the blog post.
  - `thumbnail`: Image thumbnail for the blog post.
  - `views`: Number of views the blog post has.
  - `author`: Author of the blog post.

BlogComment
^^^^^^^^^^^
The `BlogComment` model represents a comment on a blog post.

- **Fields**:
  - `customer`: The customer who posted the comment.
  - `blog`: The blog post the comment is associated with.
  - `subject`: Subject of the comment.
  - `message`: Content of the comment.
  - `active`: Boolean field indicating whether the comment is active or not.

Discount App
~~~~~~~~~~~~

BaseDiscount
^^^^^^^^^^^^
The `BaseDiscount` model represents a base discount available in the system.

- **Fields**:
  - `discount`: The discount value.
  - `active`: Boolean field indicating whether the discount is active or not.
  - `code`: Discount code (optional).
  - `valid_from`: Start date of the discount validity period.
  - `valid_to`: End date of the discount validity period.
  - `mode`: The mode of the discount.
  - `limit_price`: The minimum price required for the discount to apply.
  - `max_price`: The maximum price for which the discount is applicable.

  