GET    http://127.0.0.1:8000/api/products/products/          # list all
GET    http://127.0.0.1:8000/api/products/products/1/        # single product
GET    http://127.0.0.1:8000/api/products/products/?search=iphone    # search
GET    http://127.0.0.1:8000/api/products/products/?category=1       # filter
GET    http://127.0.0.1:8000/api/products/products/?ordering=price   # sort
GET    http://127.0.0.1:8000/api/products/categories/        # list categories

# Cart 
GET    http://127.0.0.1:8000/api/cart/                       # view cart
POST   http://127.0.0.1:8000/api/cart/add/                   # add item
POST   http://127.0.0.1:8000/api/cart/remove/                # remove item

# Orders 
GET    http://127.0.0.1:8000/api/orders/                     # list orders
POST   http://127.0.0.1:8000/api/orders/checkout/   