from classes.dimensions import Dimensions

class Product:
    def __init__(self, id, title, description, category, price, stock_status, dimensions):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.price = price
        self.stock_status = stock_status
        self.dimensions = dimensions

    def __str__(self):
        return f"Product(id={self.id}, title={self.title}, price={self.price}, stock_status={self.stock_status})"

    @classmethod
    def from_json(cls, json_data):
        dimensions_data = json_data["dimensions"]
        dimensions_obj = Dimensions(length_mm=dimensions_data["length_mm"],
                                    width_mm=dimensions_data["width_mm"],
                                    height_mm=dimensions_data["height_mm"],
                                    weight_g=dimensions_data["weight_g"])

        return cls(id=json_data["id"],
                   title=json_data["title"],
                   description=json_data["description"],
                   category=json_data["category"],
                   price=json_data["price"],
                   stock_status=json_data["stock_status"],
                   dimensions=dimensions_obj)

