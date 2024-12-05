# Written by Landry M. King, 2024
# PGData: handles connection to PostgreSQL servers

import os
import os.path
import json
import psycopg2
import psycopg2.extras

from pathlib import Path
from Config import Config

class PGData:
    def __init__(self):
        configuration = Config()

        username, password, database, host, port = configuration.getUATCreds()

        self.connection = psycopg2.connect(
            database = database,
            user = username,
            password = password,
            host = host,
            port = port
        )

        self.cursor = self.connection.cursor(cursor_factory = psycopg2.extras.DictCursor)

    def getProductData(self, sku):
        sql = "SELECT DISTINCT * FROM oro_product WHERE dt_global_item_family_id = 'indoor_air_quality' AND sku_uppercase = '{}' LIMIT 1;"
        sql = sql.format(sku)

        self.cursor.execute(sql)
        return self.cursor.fetchone()