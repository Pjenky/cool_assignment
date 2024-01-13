import requests
import logging
from classes.product import Product

def fetch_products_from_api(api_url):
    response = requests.get(api_url)

    if response.status_code == 200:
        products_data = response.json()
        products_objects = [Product.from_json(product_data) for product_data in products_data["products"]]
        return products_objects
    else:
        # There was an error with the request
        logging.error("Error: %d", response.status_code)
        logging.error("Error details: %s", response.text)
        return None

def print_product(product):
    print(f"Title: {product.title}")
    print(f"ID: {product.id}")
    print(f"Price: {product.price/100} DKK")
    print(f"Stock Status: {product.stock_status}")
    print("\n")

url = "https://shipping-mock.api.prod.coolshop.com/products"
products = fetch_products_from_api(url)

if products:
    # Find the product with the lowest price
    cheapest_product = min(products, key=lambda product: product.price)
    print("Cheapest Product:", print_product(cheapest_product))
    

    # Find the product ID with the highest price
    expensive_product = max(products, key=lambda product: product.price)
    print("Most Expensive Product:", print_product(expensive_product))

    # Find and list the products that are in stock
    in_stock_products = [product for product in products if product.stock_status == "in_stock"]
    if in_stock_products:
        print("Products In Stock:")
        for product in in_stock_products:
            print(f"ID: {product.id}")
    else:
        print("No products in stock.")
    print("\n")

    # Find the average volume of all products in cm3
    products_with_dimensions = [product for product in products if hasattr(product, 'dimensions')]
    if products_with_dimensions:
        # Calculate the average volume
        total_volume = 0
        for product in products_with_dimensions:
            dimensions = product.dimensions
            volume = dimensions.length_mm * dimensions.width_mm * dimensions.height_mm
            total_volume += volume

        # Divide by 1000 to convert from mm3 to cm3 and find the average volume
        average_volume = total_volume / 1000 / len(products_with_dimensions)

        print(f"Average Volume of Products: {average_volume} cm^3")
    else:
        print("No products with dimensions available.")

else:
    print("No products available.")
