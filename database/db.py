#!/usr/bin/python3
# -*- coding: utf-8 -*-

import mysql.connector
import hashlib


class Db:
    def __init__(self):

        self.connect = mysql.connector.connect(
            host="board",
            user="xml",
            password="xml",
            database="offers"
        )
        print('Connect to db established...')

    def InsertMany(self, data: list) -> int:

        store = data[0]['store']
        store_id = self.GetStoreIdOrCreate(store)
        if not store_id:
            raise RuntimeError('Cant get id of stores. Aborting ...')

        self.HandleOffers(data, store_id)

    def GetStoreIdOrCreate(self, store_name: str) -> int:
        result = None
        cursor = self.connect.cursor()

        sql = f"select id from stores where store_name = '{store_name}'"
        cursor.execute(sql)
        result = cursor.fetchone()

        if not result:
            sql = f"insert into stores (store_name) VALUES ('{store_name}')"
            cursor.execute(sql)
            sql = "select LAST_INSERT_ID()"
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connect.commit()
        cursor.close()

        return result[0]

    def HandleOffers(self, data: list, store_id: int):
        # final_list.append({
        #     'name': meta,
        #     'price': price,
        #     'unit': UNIT,
        #     'store': STORE,
        #     'category_id': CATEGORY_ID
        # })

        for offer in data:
            try:
                offer_id = self.GetOfferIdOrCreate(offer, store_id)

            except mysql.connector.Error as error:
                if self.connect.is_connected():
                    cursor.close()
                    self.connect.close()

                raise RuntimeError(
                    "Failed to insert into MySQL table {}".format(error))

    def GetOfferIdOrCreate(self, offer: dict, store_id: int) -> int:
        cursor = self.connect.cursor()

        sql = f"select offer_id from offers where name='{offer['name']}' and store_id={store_id}"

        cursor.execute(sql)
        result = cursor.fetchone()[0]
        cursor.close()

        if not result:
            cursor = self.connect.cursor()
            offer_id = abs(hash(s)) % (10 ** 10)

            sql = """insert into offers (offer_id, name, categoryId, unit, store_id) 
                    VALUES (%s, %s, %s, %s, %s)"""

            val = (offer_id, offer['name'], offer['category_id'],
                   offer['unit'], store_id)

            cursor.execute(sql)
            self.connect.commit()

            sql = f"select offer_id from offers where name='{offer['name']}' and store_id={store_id}"
