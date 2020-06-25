#  Copyright © 2020 NeuroByte Tech. All rights reserved.
#
#  NeuroByte Tech is the Developer Company of Rohan Mathew.
#
#  Project: PriceTracker
#  File Name: pipelines.py
#  Last Modified: 11/05/2020, 19:59

import datetime as dt
import logging as lg

import ibm_db as db
import ibm_db_dbi as dbi
import pandas as pd


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class DBPipeline(object):
    def __init__(self):
        """This initializes a pipeline to the database."""
        dsn = ""
        with open("spider/dbAuth.txt") as auth:
            for line in auth:
                dsn += line.strip()

        self.conn = db.connect(dsn, "", "")
        self.connection = dbi.Connection(self.conn)

    def process_item(self, item, spider):
        # Checking if product is already in database
        df = self.run_query(
            f"""
            SELECT COUNT(*)
            FROM ppt_products p
            WHERE p.id = {item["id"]};
            """,
            return_results=True
        )

        # Adding it if it is not
        if df.iloc[0, 0] == 0:
            self.run_query(
                f"""
                INSERT INTO ppt_products (id, brand, model, url)
                VALUES ({item["id"]}, '{item["name"]["brand"]}', '{item["name"]["model"]}', '{item["url"]}');
                """,
                return_results=False
            )

            spider.log("New product {id} added to product list".format(id=item["id"]), lg.INFO)

        # Preparing for price update
        date = str(dt.datetime.now().date())

        # Checking if entry with same price and availability has already been made - more data efficient
        # Getting last entry for product
        df = self.run_query(
            f"""
            SELECT *
            FROM ppt_prices
            WHERE product_id = {item["id"]}
            ORDER BY date DESC
            LIMIT 1;""",
            return_results=True
        )

        # If current values are different, adding entry
        add_entry = df.shape[0] == 0
        if not add_entry:
            add_entry = add_entry or not (
                    str(df["date"][0]) == date and
                    df["price"][0] == item["price"] and
                    df["available"][0] == item["available"])

        if add_entry:
            self.run_query(
                f"""
                INSERT INTO ppt_prices (date, product_id, price, available)
                VALUES ('{date}', {item["id"]}, {item["price"]}, {str(item["available"]).lower()});
                """
            )

            spider.log("New price updated for Product {id}".format(id=item["id"]), lg.INFO)

        # Finally returning the item object after processed through this pipeline.
        return item

    def run_query(self, query, return_results=False):
        if return_results:
            result_set = pd.read_sql_query(query, self.connection)
            result_set.columns = [column.lower()
                                  for column in result_set.columns]

            return result_set
        else:
            db.exec_immediate(self.conn, query)

    def open_spider(self, spider):
        spider.log("Connected to product database", lg.INFO)

        # Creating necessary tables if not present already
        table_list = [table["TABLE_NAME"].lower()
                      for table in self.connection.tables("lzx36405")]

        if "ppt_prices" not in table_list:
            if "ppt_products" not in table_list:
                db.exec_immediate(
                    self.conn,
                    """
                    CREATE TABLE ppt_products(
                        id INT NOT NULL PRIMARY KEY,
                        brand VARCHAR(50) NOT NULL,
                        model VARCHAR(150) NOT NULL,
                        url VARCHAR(1000) NOT NULL
                    );""")

                spider.log("Added products database in absence", lg.INFO)

            db.exec_immediate(
                self.conn,
                """
                CREATE TABLE ppt_prices (
                    date DATE NOT NULL,
                    product_id INT NOT NULL REFERENCES ppt_products,
                    price DOUBLE,
                    available BOOLEAN NOT NULL
                )""")

            spider.log("Added prices database in absence", lg.INFO)

    def close_spider(self, spider):
        spider.log("Closing spider", lg.INFO)

        # Closing connection to database
        try:
            db.close(self.conn)
            self.connection.close()
        except dbi.ProgrammingError:
            self.conn, self.connection = None, None
        spider.log("Closed database connection", lg.INFO)
