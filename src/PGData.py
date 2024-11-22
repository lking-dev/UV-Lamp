import os
import os.path
import json
import psycopg2
import psycopg2.extras
from pathlib import Path

class PGData:
    def __init__(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        credentials_file = open(self.path + "\\credentials.json", "r")
        credentials = json.load(credentials_file)
        credentials_file.close()

        username = credentials["username"]
        password = credentials["password"]

        self.connection = psycopg2.connect(
            database = "orodb",
            user = username,
            password = password,
            host = "10.200.104.73",
            port = 5432
        )

        self.cursor = self.connection.cursor(cursor_factory = psycopg2.extras.DictCursor)

    def getProductSKUs(self, products_json):
        products_file = open(self.path + products_json)
        products_data = json.load(products_file)
        products_file.close()

        skus = products_data["product_skus"]
        return skus
    
    def getProductData(self, sku):
        sql = "SELECT DISTINCT * FROM oro_product WHERE dt_global_item_family_id = 'indoor_air_quality' AND sku_uppercase = '{}' LIMIT 1;"
        sql = sql.format(sku)

        self.cursor.execute(sql)
        return self.cursor.fetchone()