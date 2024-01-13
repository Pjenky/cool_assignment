import unittest
from unittest.mock import MagicMock, patch
from main import fetch_products_from_api, Product

class TestProductFunctions(unittest.TestCase):
    api_url = "https://shipping-mock.api.prod.coolshop.com/products"

    @patch('requests.get')
    def test_fetch_products_from_api_success(self, mock_get):
        # Set up a mock response for a successful API call
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"products": [
            {
                "id": 1,
                "title": "Testing Product",
                "description": "This is a product for testing purposes.",
                "category": "Testing",
                "price": 999999999999,
                "stock_status": "in_stock",
                "dimensions": {
                    "length_mm": 1,
                    "width_mm": 1,
                    "height_mm": 1,
                    "weight_g": 1
                }
            },
        ]}
        mock_get.return_value = mock_response

        # Call the function and check the result
        products = fetch_products_from_api(self.api_url)
        self.assertIsNotNone(products)
        self.assertIsInstance(products[0], Product)
    
    @patch('requests.get')
    def test_fetch_products_from_api_failure(self, mock_get):
        # Set up a mock response for a failed API call
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response

        # Call the function and check the result
        products = fetch_products_from_api(self.api_url)
        self.assertIsNone(products)
    
    def test_product_from_json(self):
        # Create a sample JSON data for a product
        json_data = {
            "id": 2,
            "title": "Testing Product 2",
            "description": "This is a second product for testing purposes.",
            "category": "Testing",
            "price": 999999999999,
            "stock_status": "in_stock",
            "dimensions": {
                "length_mm": 2,
                "width_mm": 2,
                "height_mm": 2,
                "weight_g": 2
            }
        }

        # Call the class method and check the result
        product = Product.from_json(json_data)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.id, 2)
        self.assertEqual(product.title, "Testing Product 2")
        self.assertEqual(product.description, "This is a second product for testing purposes.")

if __name__ == '__main__':
    unittest.main()